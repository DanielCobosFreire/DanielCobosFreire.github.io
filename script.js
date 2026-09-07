const servicios = [
  {icono:'bi-tools', nombre:'Soporte Técnico', descripcion:'Diagnóstico, mantenimiento preventivo y correctivo, optimización y asistencia remota.', precio:'Desde $25'},
  {icono:'bi-window', nombre:'Desarrollo Web', descripcion:'Sitios responsivos para empresas y emprendimientos, enfocados en velocidad y claridad.', precio:'Por proyecto'},
  {icono:'bi-diagram-3', nombre:'Infraestructura TI', descripcion:'Redes, conectividad, actualización de equipos y planificación tecnológica.', precio:'Según alcance'},
  {icono:'bi-lightbulb', nombre:'Consultoría IT', descripcion:'Evaluación de necesidades, selección de herramientas y mejora de procesos digitales.', precio:'Por sesión'}
];

const CLAVE = 'csi_solicitudes_v2';
let solicitudes = JSON.parse(localStorage.getItem(CLAVE) || '[]');

function renderServicios(){
  document.querySelector('#serviciosGrid').innerHTML = servicios.map(s => `
    <div class="col-md-6 col-xl-3"><article class="service-card h-100"><div class="icon-box"><i class="bi ${s.icono}"></i></div><h3>${s.nombre}</h3><p>${s.descripcion}</p><strong class="price mt-auto">${s.precio}</strong></article></div>`).join('');
}
function guardar(){localStorage.setItem(CLAVE, JSON.stringify(solicitudes));}
function escapar(texto){return String(texto).replace(/[&<>'"]/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));}
function renderSolicitudes(){
  const lista=document.querySelector('#listaSolicitudes');
  document.querySelector('#contador').textContent=solicitudes.length;
  if(!solicitudes.length){lista.innerHTML='<div class="data-card text-secondary">No hay solicitudes registradas todavía.</div>';return;}
  lista.innerHTML=solicitudes.map((s,i)=>`<article class="data-card"><div class="d-flex justify-content-between gap-3"><div><span class="badge text-bg-dark mb-2">${escapar(s.categoria)}</span><h3 class="mt-0">${escapar(s.nombre)}</h3></div><button class="btn btn-sm btn-outline-danger align-self-start" data-eliminar="${i}"><i class="bi bi-trash"></i></button></div><p class="text-secondary">${escapar(s.descripcion)}</p><div class="small"><i class="bi bi-envelope me-2"></i>${escapar(s.correo)}</div></article>`).join('');
}
function mensaje(texto,tipo='danger'){const el=document.querySelector('#mensaje');el.className=`alert alert-${tipo}`;el.textContent=texto;}

document.addEventListener('DOMContentLoaded',()=>{
  renderServicios(); renderSolicitudes();
  document.querySelector('#listaSolicitudes').addEventListener('click',e=>{const b=e.target.closest('[data-eliminar]');if(!b)return;if(confirm('¿Eliminar esta solicitud?')){solicitudes.splice(Number(b.dataset.eliminar),1);guardar();renderSolicitudes();}});
  document.querySelector('#formSolicitud').addEventListener('submit',e=>{
    e.preventDefault();const form=e.currentTarget;
    if(!form.checkValidity()){form.classList.add('was-validated');mensaje('Revisa los campos obligatorios antes de continuar.');return;}
    const spinner=document.querySelector('#spinner');spinner.classList.remove('d-none');document.querySelector('#btnGuardar').disabled=true;
    setTimeout(()=>{
      solicitudes.unshift({nombre:document.querySelector('#nombre').value.trim(),correo:document.querySelector('#correo').value.trim(),categoria:document.querySelector('#categoria').value,descripcion:document.querySelector('#descripcion').value.trim(),fecha:new Date().toISOString()});
      guardar();renderSolicitudes();form.reset();form.classList.remove('was-validated');mensaje('Solicitud registrada correctamente.','success');spinner.classList.add('d-none');document.querySelector('#btnGuardar').disabled=false;
    },500);
  });
});
