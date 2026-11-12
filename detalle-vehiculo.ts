// @ts-nocheck — controlador heredado de detalle convertido a TypeScript.
document.addEventListener("DOMContentLoaded",()=>{
 const id=new URLSearchParams(location.search).get("id"), car=id ? window.OF_CARS_VEHICULOS?.[id] : undefined;
 const content=document.getElementById("detalle-contenido");
 if(!car){document.getElementById("detalle-no-encontrado").hidden=false;return;}
 document.title=`${car.name} | OF_Cars`; content.hidden=false;
 const put=(key,value)=>document.getElementById(key).textContent=value;
 put("detalle-categoria",car.category);put("detalle-titulo",car.name);put("detalle-subtitulo",`${car.year} · ${car.brand} ${car.model}`);put("detalle-precio",`$${car.price.toLocaleString("es-CO")}`);put("detalle-descripcion",car.description);put("dato-modelo",`${car.brand} ${car.model}`);put("dato-anio",car.year);put("dato-kilometraje",car.mileage);put("dato-combustible",car.fuel);put("dato-transmision",car.transmission);put("dato-tipo",car.category);
 const hero=document.getElementById("foto-principal") as HTMLImageElement, thumbs=document.getElementById("miniaturas-vehiculo")!;hero.src=car.images[0];hero.alt=car.name;
 car.images.forEach((src,index)=>{const button=document.createElement("button");button.type="button";button.className=`miniatura ${index===0?"activa":""}`;button.setAttribute("aria-label",`Ver fotografía ${index+1}`);const img=document.createElement("img");img.src=src;img.alt=`${car.name}, foto ${index+1}`;button.append(img);button.addEventListener("click",()=>{hero.src=src;thumbs.querySelectorAll(".miniatura").forEach((item)=>item.classList.remove("activa"));button.classList.add("activa")});thumbs.append(button)});
});

