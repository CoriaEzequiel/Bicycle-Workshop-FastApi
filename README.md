API para gestión integral de un taller de bicicletas
- Diseño y modelado de datos con SQLAlchemy ORM, definiendo entidades y relaciones para clientes, servicios, usuarios y roles.
- Validaciones y tipado estricto con Pydantic y Typing para garantizar la integridad y claridad de los datos.
- Autenticación y autorización seguras mediante JWT, control de acceso por roles, integración de Auth0 y validación de claims personalizadas.
- Desarrollo de endpoints RESTful con FastAPI, siguiendo principios de Clean Architecture:
 separación clara entre rutas, servicios del dominio, repositorios, esquemas de validación, lógica de configuración, seguridad y modelos de bases de datos.
- Gestión de configuración y variables de entorno centralizada con Pydantic Settings y dotenv.
- Migraciones de base de datos con Alembic.
- Persistencia de datos en PostgreSQL, combinando acceso asíncrono (asyncpg) y soporte tradicional (psycopg2-binary) para garantizar eficiencia y compatibilidad.
-Implementación de repositorios para separar el acceso a la base de datos, de la lógica de negocio, facilitando la escalabilidad y testing.
- Definición de schemas para entrada y salida de datos, asegurando contratos claros entre Front-End y Back-End.
- Servicios de dominio que encapsulan la lógica de negocio, promoviendo reutilización y mantenimiento.
- Gestión de dependencias y seguridad en EndPoints mediante FastAPI Depends.
- Estructura modular y escalable del proyecto, facilitando mantenimiento y extensión de funcionalidades.
- Documentación API generada con Swagger/OpenAPI.
