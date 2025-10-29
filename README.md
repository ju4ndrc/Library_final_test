# Sistema de Gestión de Biblioteca
---
# Descripción

  - La biblioteca necesita un sistema para gestionar su catálogo de libros y los autores.  
  - El sistema debe permitir:  
  - Registrar autores (nombre, país de origen, año de nacimiento).  
  - Registrar libros (título, ISBN, año de publicación, número de copias disponibles).  
  - Un libro puede tener múltiples autores (coautores).  
  - Un autor puede haber escrito múltiples libros.  
  - Consultar libros por autor.  
  - Consultar autores de un libro.

---
---
# Mapa de endpoints

##  Usuarios

| Endpoint | Método | Descripción | Relación |
|-----------|:------:|--------------|-----------|
| `/users/` | <span style="color:#1E90FF;">**GET**</span> | Lista todos los usuarios | N/A |
| `/users/` | <span style="color:#2ECC71;">**POST**</span> | Crea un nuevo usuario con contraseña encriptada | N/A |
| `/users/{user_id}` | <span style="color:#E67E22;">**PATCH**</span> | Actualiza datos de un usuario existente | N/A |
| `/users/delete_user/{user_id}` | <span style="color:#E74C3C;">**DELETE**</span> | Desactiva un usuario (soft delete) | N/A |
| `/users/active_user/{user_id}` | <span style="color:#E67E22;">**PATCH**</span> | Reactiva un usuario inactivo | N/A |
| `/users/active` | <span style="color:#1E90FF;">**GET**</span> | Lista todos los usuarios activos | N/A |
| `/users/inactive` | <span style="color:#1E90FF;">**GET**</span> | Lista todos los usuarios inactivos | N/A |

---

##  Autores

| Endpoint | Método | Descripción | Relación |
|-----------|:------:|--------------|-----------|
| `/authors/` | <span style="color:#2ECC71;">**POST**</span> | Crea un nuevo autor | 1:N con Books |
| `/authors/` | <span style="color:#1E90FF;">**GET**</span> | Lista todos los autores | 1:N con Books |
| `/authors/{author_id}` | <span style="color:#E67E22;">**PATCH**</span> | Actualiza un autor existente | 1:N con Books |
| `/authors/{author_id}` | <span style="color:#E74C3C;">**DELETE**</span> | Elimina un autor (borrado en cascada) | 1:N con Books |

---

##  Libros

| Endpoint | Método | Descripción | Relación |
|-----------|:------:|--------------|-----------|
| `/books/` | <span style="color:#2ECC71;">**POST**</span> | Crea un nuevo libro | N:1 con Authors |
| `/books/` | <span style="color:#1E90FF;">**GET**</span> | Lista todos los libros disponibles | N:1 con Authors |
| `/books/{book_id}` | <span style="color:#E67E22;">**PATCH**</span> | Actualiza información de un libro | N:1 con Authors |

---

##  Libreria

| Endpoint | Método | Descripción | Relación |
|-----------|:------:|--------------|-----------|
| `/library/` | <span style="color:#2ECC71;">**POST**</span> | Crea una nueva biblioteca | N/A |
| `/library/show` | <span style="color:#1E90FF;">**GET**</span> | Muestra las bibliotecas registradas | N/A |
| `/library/update_id/{library_id}` | <span style="color:#E67E22;">**PATCH**</span> | Actualiza datos de una biblioteca | N/A |

---

##  Prestamos

| Endpoint | Método | Descripción | Relación |
|-----------|:------:|--------------|-----------|
| `/lends/` | <span style="color:#2ECC71;">**POST**</span> | Registra un nuevo préstamo de libro | 1:N con Users, 1:N con Books |
| `/lends/` | <span style="color:#1E90FF;">**GET**</span> | Lista todos los préstamos realizados | 1:N con Users |
| `/lends/{lend_id}` | <span style="color:#1E90FF;">**GET**</span> | Consulta un préstamo específico | 1:N con Users |
| `/lends/{lend_id}` | <span style="color:#E67E22;">**PATCH**</span> | Actualiza la fecha de devolución y multa | 1:N con Users |
| `/lends/{lend_id}` | <span style="color:#E74C3C;">**DELETE**</span> | Elimina un préstamo existente | 1:N con Users |

---

##  Autenticacion

| Endpoint | Método | Descripción | Relación |
|-----------|:------:|--------------|-----------|
| `/auth/login` | <span style="color:#2ECC71;">**POST**</span> | Autenticación básica de usuario | N/A |
| `/` | <span style="color:#1E90FF;">**GET**</span> | Endpoint raíz para comprobar conexión | N/A |

---



###  Tecnologias usadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-336791?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

##  Documentación de Funciones Principales

---

###  `createUser(user_data: CreateUser, session: SessionDep)`

**Descripción:**  
Crea un nuevo usuario en la base de datos.

**Parámetros:**  
- `user_data`: Datos del usuario *(nombre, email, password)*  
- `session`: Sesión de base de datos  

**Retorna:**  
 Objeto `User` con contraseña encriptada.

---

###  `createAuthor(author_data: CreateAuthor, session: SessionDep)`

**Descripción:**  
Registra un nuevo autor.

**Parámetros:**  
- `author_data`: Nombre, país y año de nacimiento  
- `session`: Sesión **SQLite**

**Retorna:**  
Objeto `Author` recién creado.

---

### `create_book(book_data: CreateBook, session: SessionDep)`

**Descripción:**  
Crea un nuevo libro asociado a un autor.

**Parámetros:**  
- `book_data`: Título, ISBN, año de publicación, copias disponibles, `author_id`

**Retorna:**  
Objeto `Book` validado.

**Errores:**  
-  `404`: Si el autor no existe.

---

###  `new_lend(lend_data: CreateLend, session: SessionDep)`

**Descripción:**  
Registra un préstamo de libro a un usuario.

**Parámetros:**  
- `lend_data`: Contiene `user_id`, `book_id`, y `return_date`

**Retorna:**  
 Objeto `Lend` con el detalle del préstamo.

**Reglas:**  
-  Disminuye automáticamente las copias disponibles del libro.  
-  Lanza error si no hay copias disponibles.

---

###  `create_library(library_data: CreateLibrary, session: SessionDep)`

**Descripción:**  
Crea la biblioteca principal (solo una vez).

**Parámetros:**  
- `library_data`: Nombre y dirección de la biblioteca  

**Errores:**  
-  `400`: Si ya existe una biblioteca registrada.

---

###  Base de Datos: **SQLite**

 El archivo de base de datos se genera automáticamente al ejecutar el proyecto.  
Usa SQLModel/FastAPI para la conexión, persistencia y consultas ORM.

---
##  Instalacion y Ejecucion

```bash
# Clonar el repositorio
git clone https://github.com/user/Library_final_test.git
cd Library_final_test

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
fastapi dev main.py

```


# [Diagramas](https://lucid.app/lucidspark/3dca03c4-5868-47a2-8ed3-bb78a5bd952c/edit?page=0_0#)
# [Instalacion con Docker](https://fastapi.tiangolo.com/es/deployment/docker/?h=dock#construir-la-imagen-de-docker)
