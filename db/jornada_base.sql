CREATE TABLE `residente` (
  `id` char(6) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
   `apellidos` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
   `telefono` int(15),
    `correo` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
    `edad` int(3) COLLATE NOT NULL,
    `direccion` varchar(200) COLLATE utf8_unicode_ci,
    `comida_entregada` tinyint(1) NOT NULL,
  `observacion` varchar(600) COLLATE utf8_unicode_ci,
    `fecha` timestamp,

) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Almacena los datos de los residentes.';

ALTER TABLE `residente`
  ADD PRIMARY KEY (`id`);
COMMIT;