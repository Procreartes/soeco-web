#!/usr/bin/env python3
"""Genera la web de SOECO Canarias (soecocanarias.com).

Uso:  python3 scripts/generar.py
Datos editables (Gestor de webs del portal o a mano): data/servicios.json, data/proyectos.json, data/portada.json
No edites los .html a mano: se sobrescriben.
"""
import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from web import RAIZ, Sitio, ICO, esc, datos, mailto, imagen  # noqa: E402

CORREO = "hola@soecocanarias.com"

S = Sitio(
    nombre="SOECO Canarias", nombre_corto="SOECO",
    dominio="https://soecocanarias.com",
    titular="Asociación Medioambiental SOECO Canarias", nif="G55378210",
    domicilio="Calle Schubert, 11, puerta 17 · 35016 Las Palmas de Gran Canaria",
    correo=CORREO, correo_datos=CORREO,
    objeto="Esta web informa sobre la Asociación Medioambiental SOECO Canarias, sus servicios de sostenibilidad para eventos y la forma de contactar.",
    color_tema="#253932", color_fondo="#f4f8f6",
    precarga=["righteous-latin-400-normal.woff2", "outfit-latin-400-normal.woff2"],
    menu=[("/#que-es", "Qué es SOECO"), ("/#servicios", "Servicios"), ("/#huella", "Huella de carbono"),
          ("/#como", "Cómo trabajamos"), ("/#contacto", "Contacto")],
    marca='<img src="/img/logo.webp" width="180" height="51" alt="SOECO, Sostenibilidad y Ecología de Canarias">',
    pie_html='''<div class="pie-arriba">
      <div><img class="pie-logo" src="/img/logo-blanco.webp" width="220" height="63" alt="SOECO, Sostenibilidad y Ecología de Canarias" loading="lazy">
      <p>Asociación medioambiental · Planes de sostenibilidad y huella de carbono para eventos en Canarias</p></div>
      <div><p><a href="mailto:hola@soecocanarias.com">hola@soecocanarias.com</a></p>
      <p>Las Palmas de Gran Canaria</p></div>
    </div>''',
    credito_fotos=False,
)

SERVICIOS = datos("servicios.json", [])
PROYECTOS = datos("proyectos.json", [])

AMBITOS = [
    ("Movilidad", "Cómo llega el público, transporte público, aparcamientos y desplazamientos de artistas y equipos."),
    ("Energía", "Generadores, conexión a red y aprovechamiento de la luz natural en la programación."),
    ("Residuos", "Recogida selectiva, puntos de reciclaje y reducción de envases."),
    ("Agua", "Agua del grifo y envases reutilizables en lugar de botellas pequeñas."),
    ("Compras", "Proveedores locales, catering y materiales de producción."),
    ("Comunicación", "Menos papel y plástico: cartelería ajustada, soportes reutilizables y digitales."),
]

ALCANCES = [
    ("Alcance 1", "Emisiones directas", "Lo que se quema en el propio evento: generadores y vehículos de la organización."),
    ("Alcance 2", "Electricidad", "La energía eléctrica que consume el evento desde la red."),
    ("Alcance 3", "Emisiones indirectas", "Desplazamientos del público y de las compañías, alojamiento, catering, materiales y residuos. Suele ser la parte más grande."),
]

PASOS = [
    ("Antes", "Visitamos los espacios, conocemos la producción y redactamos el plan con sus objetivos e indicadores."),
    ("Durante", "Acompañamos la aplicación de las medidas y recogemos las evidencias: fotos, certificados, encuestas y datos de consumo."),
    ("Después", "Calculamos la huella de carbono, verificamos los resultados y entregamos los informes para la memoria de justificación."),
]

PUBLICO = ["Festivales y fiestas populares", "Eventos institucionales", "Espectáculos y giras", "Ferias y congresos", "Eventos deportivos"]


def hoja(cls=""):
    """Hoja del logotipo, decorativa (recuerda a la «e» de SOECO)."""
    return f'''<svg class="hoja {cls}" viewBox="0 0 200 200" aria-hidden="true" focusable="false">
<circle cx="100" cy="112" r="80" fill="currentColor" opacity=".16"/>
<path d="M150 18c22 40 8 104-52 118-22 5-40 18-48 34 0-38 18-74 54-90 24-11 40-30 46-62z" fill="currentColor" opacity=".5"/>
</svg>'''


def inicio():
    p = (datos("portada.json", []) or [{}])[0]
    fondo = imagen(p.get("imagen"), p.get("imagen_alt") or "", "100vw", "portada-foto", "eager")
    servicios = ""
    for i, s in enumerate(SERVICIOS):
        img = imagen(s.get("imagen"), s.get("imagen_alt") or s.get("titulo"), "(min-width: 900px) 33vw, 100vw", "servicio-foto")
        puntos = "".join(f"<li>{ICO['check']}<span>{esc(x)}</span></li>" for x in str(s.get("puntos") or "").splitlines() if x.strip())
        servicios += f'''<li class="servicio aparece">{img}<div class="servicio-txt">
      <h3>{esc(s.get("titulo"))}</h3><p>{esc(s.get("texto"))}</p>
      {f'<ul class="lista-check">{puntos}</ul>' if puntos else ""}</div></li>'''
    ambitos = "".join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in AMBITOS)
    alcances = "".join(f'<li class="alcance aparece"><span class="alcance-n">{esc(n)}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for n, t, d in ALCANCES)
    pasos = "".join(f'<li class="aparece"><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in PASOS)
    publico = "".join(f"<li>{esc(x)}</li>" for x in PUBLICO)
    proyectos = ""
    for pr in PROYECTOS:
        img = imagen(pr.get("imagen"), pr.get("imagen_alt") or pr.get("titulo"), "(min-width: 900px) 33vw, 100vw", "proyecto-foto")
        enlace = pr.get("enlace") or ""
        proyectos += f'''<li class="proyecto aparece">{img}<div class="proyecto-txt">
      {f'<p class="proyecto-anio">{esc(pr["anio"])}</p>' if pr.get("anio") else ""}<h3>{esc(pr.get("titulo"))}</h3><p>{esc(pr.get("texto"))}</p>
      {f'<a href="{esc(enlace)}" rel="noopener">Ver el evento {ICO["flecha"]}</a>' if enlace.startswith("https://") else ""}</div></li>'''
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "NGO", "name": "Asociación Medioambiental SOECO Canarias",
        "alternateName": "SOECO", "url": S.dominio + "/", "email": CORREO, "taxID": "G55378210", "areaServed": "Canarias",
        "address": {"@type": "PostalAddress", "streetAddress": "Calle Schubert, 11", "postalCode": "35016",
                    "addressLocality": "Las Palmas de Gran Canaria", "addressCountry": "ES"},
    }, ensure_ascii=False)

    cuerpo = f'''<section class="portada{" con-foto" if fondo else ""}">
  {fondo}{hoja("hoja-portada")}
  <div class="contenedor portada-grid">
    <div>
      <p class="antetitulo">Sostenibilidad y ecología de Canarias</p>
      <h1>Eventos que cuidan <span>Canarias</span>.</h1>
      <p class="entradilla">Planes de sostenibilidad, cálculo de la huella de carbono y verificación para festivales, fiestas, espectáculos y eventos.</p>
      <div class="botones">
        <a class="boton boton-claro" href="#contacto">Pedir presupuesto {ICO["flecha"]}</a>
        <a class="boton boton-linea" href="#servicios">Ver servicios</a>
      </div>
    </div>
    <div class="panel aparece" aria-label="Lo que medimos en un evento">
      <p class="panel-titulo">Lo que medimos</p>
      <ul class="panel-lista">{"".join(f"<li>{ICO['check']}<span>{esc(t)}</span></li>" for t, _ in AMBITOS)}<li>{ICO['check']}<span>Igualdad y seguridad</span></li></ul>
      <p class="panel-pie">Y la huella de carbono en sus tres alcances.</p>
    </div>
  </div>
</section>

<section class="seccion" id="que-es" aria-labelledby="t-que">
  <div class="contenedor que-grid">
    <div><p class="antetitulo">Qué es SOECO</p><h2 id="t-que">Sostenibilidad que se mide</h2></div>
    <div>
      <p class="entradilla">SOECO es el acrónimo de Sostenibilidad y Ecología de Canarias. Es una asociación medioambiental dedicada a la auditoría, gestión y organización de actividades sostenibles.</p>
      <p>Nuestro propósito es fomentar la conciencia medioambiental con herramientas prácticas: ayudar a que cada evento sea cada vez más sostenible, con el menor impacto posible en la sociedad y siempre respetuoso con el medio ambiente.</p>
      <ul class="publico">{publico}</ul>
    </div>
  </div>
</section>

<section class="seccion seccion-palida" id="servicios" aria-labelledby="t-servicios">
  <div class="contenedor">
    <div class="cabecera-seccion"><p class="antetitulo">Servicios</p><h2 id="t-servicios">Del plan inicial al informe final</h2>
    <p>Podemos encargarnos de todo el proceso o solo de la parte que necesiten.</p></div>
    <ul class="servicios">{servicios}</ul>
  </div>
</section>

<section class="seccion seccion-oscura" id="huella" aria-labelledby="t-huella">
  <div class="contenedor">
    <div class="cabecera-seccion"><p class="antetitulo">Huella de carbono</p><h2 id="t-huella">Cuánto CO₂ genera un evento</h2>
    <p>La huella de carbono suma los gases de efecto invernadero que produce el evento, expresados en toneladas de CO₂ equivalente. Se calcula en tres alcances:</p></div>
    <ol class="alcances">{alcances}</ol>
    <p class="nota-huella">Con el informe sabrán de dónde vienen sus emisiones y qué cambiar en la próxima edición para reducirlas.</p>
  </div>
</section>

<section class="seccion" id="como" aria-labelledby="t-como">
  <div class="contenedor">
    <div class="cabecera-seccion"><p class="antetitulo">Cómo trabajamos</p><h2 id="t-como">Antes, durante y después del evento</h2></div>
    <ol class="pasos">{pasos}</ol>
    <h3 class="ambitos-titulo">Qué ámbitos trabajamos</h3>
    <ul class="ambitos">{ambitos}</ul>
  </div>
</section>

<section class="seccion seccion-palida" id="regenera" aria-labelledby="t-regenera">
  <div class="contenedor regenera">
    {hoja("hoja-regenera")}
    <div><p class="antetitulo">Proyecto Reforesta SOECO</p><h2 id="t-regenera">Además de medir, regeneramos</h2>
    <p class="entradilla">Los eventos que trabajan con nosotros pueden vincularse a actuaciones de regeneración ambiental en Gran Canaria.</p>
    <p>Por ejemplo, la eliminación de rabo de gato (<i>Pennisetum setaceum</i>), una especie exótica invasora, en fincas de la zona de Bandama, dentro de un espacio natural protegido.</p></div>
  </div>
</section>

{f"""<section class="seccion" id="proyectos" aria-labelledby="t-proyectos">
  <div class="contenedor">
    <div class="cabecera-seccion"><p class="antetitulo">Proyectos</p><h2 id="t-proyectos">Eventos con los que trabajamos</h2></div>
    <ul class="proyectos">{proyectos}</ul>
  </div>
</section>""" if proyectos else ""}

<section class="seccion contacto" id="contacto" aria-labelledby="t-contacto">
  <div class="contenedor contacto-caja aparece">
    <div><p class="antetitulo">Contacto</p><h2 id="t-contacto">¿Preparan un evento?</h2>
    <p>Cuéntennos qué evento es, dónde y cuándo se celebra y si lo necesitan para un patrocinio o una subvención. Les respondemos con una propuesta.</p></div>
    <a class="boton boton-claro" href="{mailto(CORREO, "Plan de sostenibilidad para un evento")}">{ICO["mail"]} {CORREO}</a>
  </div>
</section>'''
    return S.pagina("SOECO Canarias · Planes de sostenibilidad y huella de carbono para eventos",
                    "Planes de sostenibilidad, cálculo de la huella de carbono y verificación para festivales, fiestas y eventos en Canarias.",
                    "/", cuerpo, actual="", ld=ld)


def main():
    css = (RAIZ / "css/base.css").read_text(encoding="utf-8") + "\n" + (RAIZ / "css/tema.css").read_text(encoding="utf-8")
    S.escribir("css/estilos.css", css)
    S.publicar({"index.html": inicio()})


if __name__ == "__main__":
    main()
