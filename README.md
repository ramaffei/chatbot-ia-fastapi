# POC - CHATBOT With RAG for pdf content

## Running

### Requirements
- [Python 3.13.x](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/) (Optional)
- [Docker Compose](https://docs.docker.com/compose/install/) (Optional)

Running the app using Docker (via `docker-compose`)  is recommended as it will automatically install all the dependencies, database and run the app.
Otherwise, you can run the app using VENV, but you will need to install the dependencies and database manually.

**_Note:_** Environment variables required for the app to run are located in the `.env.sample` file. Modify the file name to `.env` and fill in the values.

```shell
$ docker-compose build
$ docker-compose up app
```

<details>
<summary>Or using VENV</summary>

```bash
$ pip install -r requirements.txt
$ uvicorn --app-dir app main:app --reload
```
</details>

Then open the browser at the address: http://localhost:8000/docs

---

## Code Quality
This project provides a complete configuration for `pre-commit` using `ruff`, `isort` and `mypy`.
Between these tools, consistent quality code can be ensured.

---

## DB Migrations
This project uses [Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations.

To start up the database run the command:
```bash
$ docker-compose up db
```

And then to create and migrate the database, run the command:

```bash
$ docker-compose run migrations
```

<details>
<summary>Or using VENV</summary>

```bash 
$ alembic upgrade head
```
</details>

---

## Debugging

Setting Up Debugger for Visual Studio Code with Docker

1. Create a .vscode Folder:
   - Open your project directory in Visual Studio Code
   - Create a new folder named `.vscode` in the root of your project

2. Create launch.json File:
   - Inside the `.vscode` folder, create a new file named `launch.json`

3. Copy Contents from ._vscode/launch.json:
   - Open the `.vscode/launch.json` file, and configure it with the appropriate settings for your project. This file is used to define configurations for launching and debugging your application

4. Run the Docker Container:
   - Open a terminal.
   - Navigate to your project directory.
   - Execute the following command to start the Docker container service:

     ```bash
     $ docker-compose up debug
     ```

5. Start Debugging:
   - Set breakpoints in your code where you want to start debugging
   - Press `F5` in Visual Studio Code to start the debugging process

6. Debug Your Application:
    - Once connected, you can use the debugging features in Visual Studio Code to step through your code, inspect variables, and troubleshoot issues

---
