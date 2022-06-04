CREATE DATABASE `tsseirl_dev_educasm`;
 
/*sadasdas*/

CREATE TABLE Alumno(
	`Id` int AUTO_INCREMENT NOT NULL,
	`Nombres` varchar(150) NOT NULL,
	`ApellidoPaterno` varchar(150) NOT NULL,
	`ApellidoMaterno` varchar(150) NOT NULL,
	`IdInstitucion` int NULL,
 CONSTRAINT `PK_Alumno` PRIMARY KEY 
(
	`Id` ASC
) 
);

CREATE TABLE AlumnoCurso(
	`IdAlumno` int NOT NULL,
	`IdCurso` int NOT NULL,
	`Periodo` int NOT NULL,
	`FechaInscripcion` Datetime(6) NOT NULL,
	`IdDocente` int NOT NULL DEFAULT 0,
 CONSTRAINT `PK_AlumnoCurso` PRIMARY KEY 
(
	`IdAlumno` ASC,
	`IdCurso` ASC,
	`Periodo` ASC
) 
);

CREATE TABLE Cuestionario(
	`Id` int AUTO_INCREMENT NOT NULL,
	`IdDocente` int NOT NULL,
	`FechaDisponible` Datetime(6) NOT NULL,
	`FechaExpiracion` Datetime(6) NULL,
	`IdCurso` int NOT NULL DEFAULT 0,
	`Nombre` varchar(255) NULL,
 CONSTRAINT `PK_Cuestionario` PRIMARY KEY 
(
	`Id` ASC
) 
);

CREATE TABLE CuestionarioPregunta(
	`IdCuestionario` int NOT NULL,
	`IdPregunta` int NOT NULL,
	`Puntaje` decimal(10, 2) NOT NULL DEFAULT 0.0,
	`Reintentos` int NOT NULL DEFAULT 1,
 CONSTRAINT `PK_CuestionarioPregunta` PRIMARY KEY 
(
	`IdCuestionario` ASC,
	`IdPregunta` ASC
) 
);

CREATE TABLE Curso(
	`Id` int AUTO_INCREMENT NOT NULL,
	`Descripcion` varchar(150) NOT NULL,
	`IdNivel` int NOT NULL,
	`IdInstitucion` int NULL,
 CONSTRAINT `PK_Curso` PRIMARY KEY 
(
	`Id` ASC
) 
);


CREATE TABLE Docente(
	`Id` int AUTO_INCREMENT NOT NULL,
	`Nombres` varchar(150) NOT NULL,
	`ApellidoPaterno` varchar(150) NOT NULL,
	`ApellidoMaterno` varchar(150) NOT NULL,
 CONSTRAINT `PK_Docente` PRIMARY KEY 
(
	`Id` ASC
) 
);


CREATE TABLE DocenteCurso(
	`IdInstitucion` int NOT NULL,
	`IdDocente` int NOT NULL,
	`IdCurso` int NOT NULL,
 CONSTRAINT `PK_DocenteCurso` PRIMARY KEY 
(
	`IdInstitucion` ASC,
	`IdDocente` ASC,
	`IdCurso` ASC
) 
);


CREATE TABLE Institucion(
	`Id` int AUTO_INCREMENT NOT NULL,
	`Nombre` varchar(255) NOT NULL,
 CONSTRAINT `PK_Institucion` PRIMARY KEY 
(
	`Id` ASC
) 
);


CREATE TABLE InstitucionDocente(
	`IdInstitucion` int NOT NULL,
	`IdDocente` int NOT NULL,
 CONSTRAINT `PK_InstitucionDocente` PRIMARY KEY 
(
	`IdInstitucion` ASC,
	`IdDocente` ASC
) 
);


CREATE TABLE Nivel(
	`Id` int AUTO_INCREMENT NOT NULL,
	`Descripcion` varchar(150) NOT NULL,
 CONSTRAINT `PK_Nivel` PRIMARY KEY 
(
	`Id` ASC
) 
);


CREATE TABLE Pregunta(
	`Id` int AUTO_INCREMENT NOT NULL,
	`Texto` varchar(250) NOT NULL,
	`Tipo` Longtext NULL,
	`IdCurso` int NOT NULL DEFAULT 0,
	`IdDocente` int NOT NULL DEFAULT 0,
	`IdInstitucion` int NOT NULL DEFAULT 0,
 CONSTRAINT `PK_Pregunta` PRIMARY KEY 
(
	`Id` ASC
) 
);


CREATE TABLE PreguntaOpcion(
	`Id` int AUTO_INCREMENT NOT NULL,
	`Texto` varchar(250) NOT NULL,
	`Correcta` Tinyint NOT NULL,
	`IdPregunta` int NOT NULL,
 CONSTRAINT `PK_PreguntaOpcion` PRIMARY KEY 
(
	`Id` ASC
) 
);


CREATE TABLE Recurso(
	`Id` int AUTO_INCREMENT NOT NULL,
	`Descripcion` varchar(500) NOT NULL,
	`Contenido` varchar(500) NOT NULL,
	`Tipo` nchar(1) NOT NULL,
	`IdInstitucion` int NOT NULL,
	`OriginalFilename` varchar(500) NULL,
	`Miniatura` Longtext NULL,
	`Titulo` varchar(500) NOT NULL DEFAULT N'',
 CONSTRAINT `PK_Recurso` PRIMARY KEY 
(
	`Id` ASC
) 
);


CREATE TABLE SolucionCuestionario(
	`Id` int AUTO_INCREMENT NOT NULL,
	`IdAlumno` int NOT NULL,
	`IdCuestionario` int NOT NULL,
	`FechaSolucion` Datetime(6) NOT NULL,
	`FechaRevision` Datetime(6) NULL,
 CONSTRAINT `PK_SolucionCuestionario` PRIMARY KEY 
(
	`Id` ASC
) 
);


CREATE TABLE SolucionPregunta(
	`Id` int AUTO_INCREMENT NOT NULL,
	`IdPregunta` int NOT NULL,
	`Respuesta` varchar(250) NOT NULL,
	`Puntaje` decimal(10, 2) NULL,
	`IdSolucion` int NOT NULL DEFAULT 0,
	`Intentos` int NOT NULL DEFAULT 0,
	`IdOpcion` int NULL,
	`IntentosPosibles` int NOT NULL DEFAULT 0,
	`PuntajePregunta` decimal(18, 2) NOT NULL DEFAULT 0.0,
 CONSTRAINT `PK_SolucionPregunta` PRIMARY KEY 
(
	`Id` ASC
) 
);


CREATE TABLE Usuario(
	`Id` int AUTO_INCREMENT NOT NULL,
	`Email` varchar(50) NOT NULL,
	`Password` varchar(250) NOT NULL,
	`Roles` varchar(250) NOT NULL,
	`Locked` Tinyint NOT NULL,
	`Token` Char(36) NULL,
	`TokenExpiration` Datetime(6) NULL,
	`IdAlumno` int NULL,
	`IdDocente` int NULL,
 CONSTRAINT `PK_Usuario` PRIMARY KEY 
(
	`Id` ASC
) 
);



ALTER TABLE Alumno  ADD  CONSTRAINT `FK_Alumno_Institucion_IdInstitucion` FOREIGN KEY(`IdInstitucion`)
REFERENCES Institucion (`Id`);
 
ALTER TABLE AlumnoCurso  ADD  CONSTRAINT `FK_AlumnoCurso_Alumno_IdAlumno` FOREIGN KEY(`IdAlumno`)
REFERENCES Alumno (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE AlumnoCurso  ADD  CONSTRAINT `FK_AlumnoCurso_Curso_IdCurso` FOREIGN KEY(`IdCurso`)
REFERENCES Curso (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE AlumnoCurso  ADD  CONSTRAINT `FK_AlumnoCurso_Docente_IdDocente` FOREIGN KEY(`IdDocente`)
REFERENCES Docente (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE Cuestionario  ADD  CONSTRAINT `FK_Cuestionario_Curso_IdCurso` FOREIGN KEY(`IdCurso`)
REFERENCES Curso (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE Cuestionario  ADD  CONSTRAINT `FK_Cuestionario_Docente_IdDocente` FOREIGN KEY(`IdDocente`)
REFERENCES Docente (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE CuestionarioPregunta  ADD  CONSTRAINT `FK_CuestionarioPregunta_Cuestionario_IdCuestionario` FOREIGN KEY(`IdCuestionario`)
REFERENCES Cuestionario (`Id`);
 
ALTER TABLE CuestionarioPregunta  ADD  CONSTRAINT `FK_CuestionarioPregunta_Pregunta_IdPregunta` FOREIGN KEY(`IdPregunta`)
REFERENCES Pregunta (`Id`);
 
ALTER TABLE Curso  ADD  CONSTRAINT `FK_Curso_Institucion_IdInstitucion` FOREIGN KEY(`IdInstitucion`)
REFERENCES Institucion (`Id`);
 
ALTER TABLE Curso  ADD  CONSTRAINT `FK_Curso_Nivel_IdNivel` FOREIGN KEY(`IdNivel`)
REFERENCES Nivel (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE DocenteCurso  ADD  CONSTRAINT `FK_DocenteCurso_Curso_IdCurso` FOREIGN KEY(`IdCurso`)
REFERENCES Curso (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE DocenteCurso  ADD  CONSTRAINT `FK_DocenteCurso_Docente_IdDocente` FOREIGN KEY(`IdDocente`)
REFERENCES Docente (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE DocenteCurso  ADD  CONSTRAINT `FK_DocenteCurso_Institucion_IdInstitucion` FOREIGN KEY(`IdInstitucion`)
REFERENCES Institucion (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE InstitucionDocente  ADD  CONSTRAINT `FK_InstitucionDocente_Docente_IdDocente` FOREIGN KEY(`IdDocente`)
REFERENCES Docente (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE InstitucionDocente  ADD  CONSTRAINT `FK_InstitucionDocente_Institucion_IdInstitucion` FOREIGN KEY(`IdInstitucion`)
REFERENCES Institucion (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE Pregunta  ADD  CONSTRAINT `FK_Pregunta_Curso_IdCurso` FOREIGN KEY(`IdCurso`)
REFERENCES Curso (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE Pregunta  ADD  CONSTRAINT `FK_Pregunta_Docente_IdDocente` FOREIGN KEY(`IdDocente`)
REFERENCES Docente (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE Pregunta  ADD  CONSTRAINT `FK_Pregunta_Institucion_IdInstitucion` FOREIGN KEY(`IdInstitucion`)
REFERENCES Institucion (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE PreguntaOpcion  ADD  CONSTRAINT `FK_PreguntaOpcion_Pregunta_IdPregunta` FOREIGN KEY(`IdPregunta`)
REFERENCES Pregunta (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE Recurso  ADD  CONSTRAINT `FK_Recurso_Institucion_IdInstitucion` FOREIGN KEY(`IdInstitucion`)
REFERENCES Institucion (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE SolucionCuestionario  ADD  CONSTRAINT `FK_SolucionCuestionario_Alumno_IdAlumno` FOREIGN KEY(`IdAlumno`)
REFERENCES Alumno (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE SolucionCuestionario  ADD  CONSTRAINT `FK_SolucionCuestionario_Cuestionario_IdCuestionario` FOREIGN KEY(`IdCuestionario`)
REFERENCES Cuestionario (`Id`)
ON DELETE CASCADE;

ALTER TABLE SolucionPregunta  ADD  CONSTRAINT `FK_SolucionPregunta_Pregunta_IdPregunta` FOREIGN KEY(`IdPregunta`)
REFERENCES Pregunta (`Id`)
ON DELETE CASCADE;
 
ALTER TABLE SolucionPregunta  ADD  CONSTRAINT `FK_SolucionPregunta_PreguntaOpcion_IdOpcion` FOREIGN KEY(`IdOpcion`)
REFERENCES PreguntaOpcion (`Id`);
 
 
ALTER TABLE SolucionPregunta  ADD  CONSTRAINT `FK_SolucionPregunta_SolucionCuestionario_IdSolucion` FOREIGN KEY(`IdSolucion`)
REFERENCES SolucionCuestionario (`Id`);
 
ALTER TABLE Usuario  ADD  CONSTRAINT `FK_Usuario_Alumno_IdAlumno` FOREIGN KEY(`IdAlumno`)
REFERENCES Alumno (`Id`);
 

ALTER TABLE Usuario  ADD  CONSTRAINT `FK_Usuario_Docente_IdDocente` FOREIGN KEY(`IdDocente`)
REFERENCES Docente (`Id`);

