#!/usr/bin/env ruby
# ---------------------------------------------------------------------------
# Trae los datos del sitio de aguas a este sitio, agregándoles `areas: [aguas]`.
#
# No inventa nada: copia entradas de _data/*.yml del repo de aguas, les pone el
# campo de área y las fusiona acá. Es idempotente — si una entrada ya existe
# (mismo id, o mismo título en el caso de publicaciones), la salta.
#
#   cd ~/Library/CloudStorage/Dropbox/pagina_web_gtech_general/github
#   ruby herramientas/migrar-aguas.rb            # muestra qué haría
#   ruby herramientas/migrar-aguas.rb --escribir # lo hace
#
# Cambia ORIGEN si el repo de aguas está en otra ruta.
# ---------------------------------------------------------------------------

require "yaml"
require "date"
require "fileutils"

ORIGEN  = ENV.fetch("ORIGEN",
  File.expand_path("~/Library/CloudStorage/Dropbox/pagina_web_gtech/github/_data"))
DESTINO = File.expand_path("../_data", __dir__)
AREA    = ENV.fetch("AREA", "aguas")
ESCRIBIR = ARGV.include?("--escribir")

ARCHIVOS = %w[people.yml projects.yml collaborations.yml research.yml news.yml
              alumni.yml publications.yml]

def cargar(ruta)
  return nil unless File.exist?(ruta)
  YAML.safe_load(File.read(ruta), permitted_classes: [Date], aliases: true)
end

def clave(entrada)
  entrada["id"] || entrada["name"] || entrada["title"] || entrada.to_s
end

def con_area(entrada)
  e = entrada.dup
  actuales = Array(e["areas"])
  e["areas"] = (actuales + [AREA]).uniq
  # `areas` primero, para que se lea de inmediato al abrir el archivo
  { "areas" => e.delete("areas") }.merge(e)
end

unless Dir.exist?(ORIGEN)
  abort "No encuentro el sitio de aguas en:\n  #{ORIGEN}\nDefine ORIGEN=... y vuelve a correr."
end

resumen = []

ARCHIVOS.each do |archivo|
  origen  = cargar(File.join(ORIGEN, archivo))
  next resumen << [archivo, "no existe en el origen", 0] if origen.nil?

  destino = cargar(File.join(DESTINO, archivo))

  nuevo, agregadas =
    if archivo == "publications.yml"
      # Estructura distinta: hash con group_authors + indexed
      d = destino || { "group_authors" => [], "indexed" => [] }
      ya = Array(d["indexed"]).map { |x| clave(x) }
      entran = Array(origen["indexed"]).reject { |x| ya.include?(clave(x)) }.map { |x| con_area(x) }
      d["group_authors"] = (Array(d["group_authors"]) + Array(origen["group_authors"])).uniq
      d["indexed"] = Array(d["indexed"]) + entran
      [d, entran.size]
    else
      d = Array(destino)
      ya = d.map { |x| clave(x) }
      entran = Array(origen).reject { |x| ya.include?(clave(x)) }.map { |x| con_area(x) }
      [d + entran, entran.size]
    end

  resumen << [archivo, "#{agregadas} entradas nuevas", agregadas]

  next unless ESCRIBIR && agregadas > 0

  ruta = File.join(DESTINO, archivo)
  FileUtils.cp(ruta, "#{ruta}.bak") if File.exist?(ruta)
  File.write(ruta, "# Actualizado por herramientas/migrar-aguas.rb el #{Date.today}\n" + nuevo.to_yaml)
end

puts ESCRIBIR ? "Escrito en #{DESTINO} (copias .bak de lo anterior):" : "Simulación — nada se escribió:"
resumen.each { |a, msg, _| puts "  #{a.ljust(24)} #{msg}" }

puts <<~AVISO

  Después de correr esto, a mano:
    · copiar las fotos de assets/img/{people,news} del sitio de aguas a este repo
    · revisar que los comentarios de cabecera de cada _data/*.yml sigan ahí
      (to_yaml los borra: por eso quedan los .bak)
    · validar:  ruby -ryaml -rdate -e 'Dir.glob("_data/*.yml").each { |f|
        YAML.safe_load(File.read(f), permitted_classes:[Date]); puts "OK #{f}" }'
AVISO
