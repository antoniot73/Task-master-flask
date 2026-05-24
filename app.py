"""
Aplicación CRUD Task Master personalizada con Flask + SQLite3.

Este proyecto reproduce el ejercicio del tutorial solicitado y agrega una
personalización funcional: prioridad de tareas y estado de completado.

Ejecución local:
    python app.py
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()


def configure_logging() -> None:
    """
    Configura la bitácora de eventos de la aplicación.

    Returns:
        None.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def create_app() -> Flask:
    """
    Crea y configura la aplicación Flask.

    Returns:
        Flask: Instancia configurada de la aplicación.
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    register_routes(app)

    with app.app_context():
        db.create_all()
        logging.info("Base de datos inicializada correctamente.")

    return app


class Todo(db.Model):
    """
    Modelo relacional para almacenar tareas.

    Attributes:
        id: Identificador único de la tarea.
        content: Descripción de la tarea.
        priority: Nivel de prioridad asignado.
        completed: Estado lógico de finalización.
        date_created: Fecha y hora de creación.
    """

    id: int = db.Column(db.Integer, primary_key=True)
    content: str = db.Column(db.String(200), nullable=False)
    priority: str = db.Column(db.String(20), nullable=False, default="Media")
    completed: bool = db.Column(db.Boolean, nullable=False, default=False)
    date_created: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """
        Devuelve una representación depurable de la tarea.

        Returns:
            str: Representación textual del objeto.
        """
        return f"<Todo id={self.id} content={self.content!r}>"


def validate_task_content(content: str) -> bool:
    """
    Valida que el contenido de la tarea tenga longitud mínima.

    Args:
        content: Texto capturado desde el formulario.

    Returns:
        bool: True si el texto es válido, False en caso contrario.
    """
    return bool(content and len(content.strip()) >= 3)


def get_all_tasks() -> list[Todo]:
    """
    Consulta todas las tareas ordenadas por fecha de creación.

    Returns:
        list[Todo]: Lista de tareas registradas.
    """
    return Todo.query.order_by(Todo.date_created).all()


def register_routes(app: Flask) -> None:
    """
    Registra las rutas principales de la aplicación.

    Args:
        app: Instancia Flask sobre la cual se registran las rutas.

    Returns:
        None.
    """

    @app.route("/", methods=["GET", "POST"])
    def index() -> str:
        """
        Renderiza la página principal y procesa nuevas tareas.

        Returns:
            str: Plantilla HTML renderizada o redirección.
        """
        if request.method == "POST":
            task_content = request.form.get("content", "")
            task_priority = request.form.get("priority", "Media")

            if not validate_task_content(task_content):
                logging.warning("Intento de crear tarea con contenido inválido.")
                tasks = get_all_tasks()
                return render_template(
                    "index.html",
                    tasks=tasks,
                    error="La tarea debe contener al menos 3 caracteres.",
                )

            new_task = Todo(content=task_content.strip(), priority=task_priority)

            try:
                db.session.add(new_task)
                db.session.commit()
                logging.info("Tarea creada: %s", new_task)
                return redirect(url_for("index"))
            except Exception as exc:
                db.session.rollback()
                logging.exception("Error al crear tarea: %s", exc)
                tasks = get_all_tasks()
                return render_template(
                    "index.html",
                    tasks=tasks,
                    error="No fue posible agregar la tarea.",
                )

        tasks = get_all_tasks()
        return render_template("index.html", tasks=tasks, error=None)

    @app.route("/delete/<int:id>")
    def delete(id: int) -> Any:
        """
        Elimina una tarea por identificador.

        Args:
            id: Identificador de la tarea.

        Returns:
            Any: Redirección a la página principal.
        """
        task_to_delete = Todo.query.get_or_404(id)

        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            logging.info("Tarea eliminada: id=%s", id)
            return redirect(url_for("index"))
        except Exception as exc:
            db.session.rollback()
            logging.exception("Error al eliminar tarea: %s", exc)
            return "Hubo un problema al eliminar la tarea."

    @app.route("/update/<int:id>", methods=["GET", "POST"])
    def update(id: int) -> str:
        """
        Actualiza una tarea existente.

        Args:
            id: Identificador de la tarea.

        Returns:
            str: Plantilla HTML renderizada o redirección.
        """
        task = Todo.query.get_or_404(id)

        if request.method == "POST":
            task_content = request.form.get("content", "")
            task_priority = request.form.get("priority", "Media")
            task_completed = request.form.get("completed") == "on"

            if not validate_task_content(task_content):
                logging.warning("Intento de actualizar tarea con contenido inválido.")
                return render_template(
                    "update.html",
                    task=task,
                    error="La tarea debe contener al menos 3 caracteres.",
                )

            task.content = task_content.strip()
            task.priority = task_priority
            task.completed = task_completed

            try:
                db.session.commit()
                logging.info("Tarea actualizada: id=%s", id)
                return redirect(url_for("index"))
            except Exception as exc:
                db.session.rollback()
                logging.exception("Error al actualizar tarea: %s", exc)
                return render_template(
                    "update.html",
                    task=task,
                    error="No fue posible actualizar la tarea.",
                )

        return render_template("update.html", task=task, error=None)

    @app.route("/complete/<int:id>")
    def complete(id: int) -> Any:
        """
        Alterna el estado de completado de una tarea.

        Args:
            id: Identificador de la tarea.

        Returns:
            Any: Redirección a la página principal.
        """
        task = Todo.query.get_or_404(id)

        try:
            task.completed = not task.completed
            db.session.commit()
            logging.info("Estado completado alternado: id=%s", id)
            return redirect(url_for("index"))
        except Exception as exc:
            db.session.rollback()
            logging.exception("Error al cambiar estado: %s", exc)
            return "Hubo un problema al cambiar el estado de la tarea."


configure_logging()
app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=8000)
