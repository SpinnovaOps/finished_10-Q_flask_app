from flask import Flask
from app.controllers import auth_controller, file_controller, extraction_controller

def init_app(app):
    # Authentication endpoints
    app.route("/auth/signin", methods=["POST"])(auth_controller.signup)
    app.route("/auth/login", methods=["POST"])(auth_controller.login)
    app.route("/auth/logout", methods=["POST"])(auth_controller.logout)

    # File management endpoints
    app.route("/file/upload", methods=["POST"])(file_controller.upload_file)
    app.route("/file/list", methods=["GET"])(file_controller.list_uploaded_files)

    # Extraction endpoints
    app.route("/extract/custom", methods=["POST"])(extraction_controller.list_sections)
    app.route("/extract/section", methods=["POST"])(extraction_controller.extract_section_content)