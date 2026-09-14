# G-Tech — Green Technologies Research Group

Sitio paraguas del grupo, con **Jekyll** y **GitHub Pages**. Bilingüe español /
inglés, sin base de datos: todo el contenido vive en archivos YAML de `_data/`.

- **En línea:** https://faclopez91.github.io
- **Material fuente:** `../informacion/` — fuera del repositorio, no se publica.

---

## La idea de fondo: un contenido, muchas vistas

El sitio cubre cinco áreas con distinto director. Para que no se convierta en
cinco sitios pegados, **nada se escribe dos veces**:

1. Cada entrada de `_data/` lleva un campo **`areas:`**, que es una **lista** de
   ids de `areas.yml`.
2. Las páginas globales (Investigación, Proyectos, Publicaciones, Equipo,
   Noticias) muestran todo, agrupado por área.
3. La página de cada área **no se escribe**: `_layouts/area.html` filtra esas
   mismas listas por el `area_id` que declara el archivo de la página.

Un paper firmado por dos directores lleva las dos áreas y aparece en las dos sin
duplicarse. Un estudiante que trabaja con dos, igual.

```
_data/areas.yml   ─┐
_data/people.yml   ├─→  /equipo/        todo, agrupado por área
_data/projects.yml ├─→  /areas/aguas/   solo lo que tiene areas: [aguas]
_data/…            ┘    /areas/scott/   solo lo que tiene areas: [scott]
```

## Agregar un área

1. Un bloque en `_data/areas.yml` (id, director, color, nombre, bajada).
2. La persona que la dirige en `_data/people.yml`, con `group: lead`.
3. Dos archivos de cuatro líneas: `areas/<id>.html` y `en/areas/<id>.html`.

El menú, la portada, el pie y la página del área salen solos.

## Qué edito para…

| Quiero… | Archivo |
|---|---|
| agregar a alguien | `_data/people.yml` — `group` decide la sección, `areas` el área, y tener o no `bio` decide el formato (ficha ancha o tarjeta compacta) |
| agregar un proyecto | `_data/projects.yml` — el `title` va tal cual la postulación, sin traducir; `abstract` vacío |
| agregar un paper | `_data/publications.yml`, bloque `indexed`, y el apellido en `group_authors` para que salga en negrita |
| agregar una noticia | `_data/news.yml` — el texto no se escribe: se elige una plantilla de `news.templates` con `template:` (índice distinto al de la anterior del mismo tipo) |
| cambiar una línea de investigación | `_data/research.yml` — se escriben más amplias que los proyectos vigentes, a propósito |
| cambiar un texto de interfaz | `_data/es.yml` **y** su gemelo `_data/en.yml` |
| cambiar correo, dirección, cifras | `_config.yml` |
| mover a alguien a ex integrantes | quitarlo de `people.yml`, agregarlo a `alumni.yml` |

`photo: ""` muestra las iniciales. Cualquier campo vacío desaparece de la página
en vez de dejar un hueco, así que se puede publicar con datos incompletos e ir
completando.

## Traer los datos del sitio de aguas

```bash
ruby herramientas/migrar-aguas.rb              # simula
ruby herramientas/migrar-aguas.rb --escribir   # copia y agrega areas: [aguas]
```

Lee `_data/*.yml` del repo de aguas, agrega el campo de área y fusiona sin
duplicar. Deja `.bak` de lo anterior. Las fotos se copian a mano.

## Ver y publicar

```bash
bundle install                 # solo la primera vez
bundle exec jekyll serve       # http://127.0.0.1:4000
```

Validar los YAML sin Jekyll:

```bash
ruby -ryaml -rdate -e 'Dir.glob("_data/*.yml").each { |f|
  YAML.safe_load(File.read(f), permitted_classes:[Date]); puts "OK #{f}" }'
```

El `permitted_classes: [Date]` hace falta porque `news.yml` trae fechas.

Publicar: `git add -A && git commit -m "…" && git push`. GitHub Pages recompila
solo en un par de minutos.

## Notas de operación

- Esta carpeta vive dentro de Dropbox. Para que no toque el historial de git:
  `xattr -w com.dropbox.ignored 1 .git`. Una máquina a la vez, y `push` antes de
  cambiar de equipo.
- La URL está en `_config.yml` (`url` + `baseurl`). Todos los enlaces del sitio
  usan `relative_url`, así que mudarlo a otra cuenta u organización es cambiar
  esas dos líneas.
- `informacion/` va **fuera** del repositorio, un nivel por encima: ningún
  `git add` puede alcanzarla. Lo sensible no puede llegar al repo porque no está
  en él.
