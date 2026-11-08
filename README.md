# SOECO Canarias — soecocanarias.com

Web estática de la Asociación Medioambiental SOECO Canarias: planes de sostenibilidad y huella de carbono para eventos.

- Datos editables desde el Gestor de webs del portal de Grupo Livon (o a mano): `data/servicios.json`, `data/proyectos.json`, `data/portada.json`.
- `scripts/generar.py` crea las páginas; la acción de GitHub lo ejecuta al cambiar los datos. No edites los `.html` a mano.
- Colores, logo y tipografía, según el manual de identidad de SOECO. Publicada en Cloudflare Workers (`wrangler.jsonc`).
