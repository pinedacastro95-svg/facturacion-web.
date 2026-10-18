# Sistema de facturación web — inicio

Plantilla inicial para una aplicación web adaptable a celular y computadora.

## Incluye
- Inicio de sesión con Supabase Auth.
- Panel inicial.
- Clientes: alta y listado.
- Facturas internas de servicios ocasionales o recurrentes, con frecuencia y vencimiento.
- Registro de pagos parciales o totales y cálculo del saldo pendiente.
- La frecuencia queda registrada, pero la generación automática de facturas futuras aún no está implementada.
- Esquema SQL con Row Level Security (RLS).

**Importante:** esta plantilla es un punto de partida técnico, no un sistema fiscal certificado ni listo para producción. No usar para emitir facturas tributarias oficiales hasta validar los requisitos aplicables en Nicaragua.

## Requisitos
- Node.js LTS y npm
- Una cuenta/proyecto en Supabase
- Una cuenta de alojamiento web (por ejemplo Vercel)

## 1. Preparar Supabase
1. Crear un proyecto en Supabase.
2. Abrir SQL Editor.
3. Ejecutar el contenido de `supabase/schema.sql`.
4. En Authentication > URL Configuration, configurar la URL local y la URL final del sitio cuando estén disponibles.
5. Copiar Project URL y anon/public key desde Project Settings > API.

## 2. Configurar y ejecutar
1. Descomprimir el ZIP.
2. En la carpeta del proyecto ejecutar:
   ```bash
   npm install
   ```
3. Copiar `.env.example` como `.env` y completar los valores de Supabase:
   ```bash
   npm run dev
   ```
4. Abrir la URL local que indique Vite, normalmente `http://localhost:5173`.

Nunca coloques la `service_role` key en el navegador ni en archivos `.env` que se publiquen.

## 3. Publicar
Subir el proyecto a un repositorio Git y conectarlo a Vercel. Añadir las variables `VITE_SUPABASE_URL` y `VITE_SUPABASE_ANON_KEY` en la configuración del proyecto de Vercel.

## Alcance de esta primera versión
- Un administrador inicia sesión.
- Los datos se asocian al usuario autenticado.
- Clientes, facturas internas de servicios ocasionales/recurrentes y registro de pagos parciales o totales.
- La frecuencia recurrente se guarda como dato, pero aún no hay generación automática programada de facturas futuras.
- No incluye todavía PDF, impuestos configurables, anulaciones auditadas, recuperación de contraseña ni integración con DGI.

Antes de usar con datos reales, probar permisos, configurar copias de seguridad, recuperación de contraseña, políticas de retención y validar la numeración de facturas.
