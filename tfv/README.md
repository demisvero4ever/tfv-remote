# TFV Remote (Tampa FL VoIP Remote)

Fork de [RustDesk](https://github.com/rustdesk/rustdesk) 1.5.0 (commit `fada664`) con la marca de Tampa FL VoIP
y servidor propio. Licencia AGPL-3.0, igual que el original: este repositorio es público por eso.

## Qué cambia respecto a RustDesk

- Servidor: `remote.tampaflvoip.com` con su clave pública (en `libs/hbb_common/src/config.rs`).
- Nombre interno `TFVRemote`; nombres visibles "Tampa FL VoIP Remote" / "TFV Remote".
- Identificador `com.tampaflvoip.remote` (Android e iOS) e iconos propios.
- `libs/hbb_common` va incluido en el repo (no como submódulo) porque lleva la configuración del servidor.
- El cliente nunca descarga actualizaciones de RustDesk (`src/updater.rs`).
- Workflows: solo `tfv-build.yml` (manual). Compila Windows x64, macOS (Intel y Apple), Android y Linux x64,
  y sube los instaladores a la publicación con la etiqueta indicada.

## Compilar

GitHub → Actions → "TFV Remote - compilar" → Run workflow.

## Volver a aplicar la marca sobre un RustDesk nuevo

    python3 -I tfv/apply_branding.py <carpeta-de-rustdesk>

La clave PRIVADA del servidor nunca va en este repositorio.
