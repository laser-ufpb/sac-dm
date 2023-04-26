async function carregarDispositivo(){
    const response = await axios.get('http://127.0.0.1:8000/dispositivos')
	const lista = document.getElementById('lista-dispositivo')
    const dispositivo = response.data
    dispositivo.forEach(dispositivo => {
        const item = document.createElement('li')

        item.innerText = "ID do dispositivo: " + dispositivo.id + "\n Data(atual): " + dispositivo.time_stamp 
            +"\nIntervalo de tempo: " + dispositivo.intervalo_tempo + " /ms" + "\n Densidade de máximos: " + dispositivo.densidade_maximos

        chooseColor(item,dispositivo)

        lista.appendChild(item)
        
    });
}

function chooseColor(item,dispositivo){
    if(dispositivo.densidade_maximos > 2){
        item.style.color = 'green'
    }else
        item.style.color = 'red'
}

function app(){
    console.log("App iniciada")
    carregarDispositivo()
}

app()