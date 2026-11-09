console.log("Arnaud Tadonkeng")
// collect items from the form
const itemForm = document.querySelector('#itemForm')

// add an event to the form
itemForm.addEventListener("submit", async function(event){
    event.preventDefault()
    const name = document.querySelector('#name').value
    const price = document.querySelector('#price').value

    try{
        // await to pause request until the request finishes
        //fetch() sends an HTTP request to a server
        const res = await fetch("http://127.0.0.1:5000/items", {method: 'POST', headers: {"Content-type":"application/json"},
            body: JSON.stringify({name:name, price:Number(price)})
        }
        )
        const data = await res.json()
        document.querySelector('#response').innerText = "Response: " + JSON.stringify(data)
    }
    catch(error){
        document.querySelector('#response').innerText = "Error: " + error
    }
})

//LOADING ALL ITEMS
async function loaditems(){
    const res = await fetch("http://127.0.0.1:5000/items")
    const data = await res.json()

    // collect the elements to print all items
    const list = document.querySelector('.itemslist')
    
    // use a loop to place each tem in the json data to a list
    for (const id in data){
        const item = data[id]
        const li = document.createElement('li')
        li.innerHTML = `
        ID = ${id}, name = ${item.name}, price = ${item.price}
        <button onclick = "showupdateform('${id}', '${item.name}', '${item.price}')"> Update </button>
        <button onclick ="deleteitem('${id})">Delete</button>
        `

        list.appendChild(li)
    }
}
// function to collect the selected item, id, and price
function showupdateform(id, name, price){
    document.querySelector("#updatesection").computedStyleMap.display = "block"
    document.querySelector('#updateName').value = name
    document.querySelector("#updateID").value = id
    document.querySelector("updatePrice").value = price
}

// function to update the selected item name and or price
async function updateItem(){
    const id = document.querySelector("#updateID").value
    const name = document.querySelector("#updateName").value
    const price = document.querySelector("#updatePrice").value
    
    // update the json data in the localhost
    const res = await fetch(`http://127.0.0.1:5000/items/${id}`, {
        method: "PUT",
        headers: {"Content-type" : "application/json"},
        body: JSON.stringify({name: name, price: Number(price)})
    })
    const html = await res.text()
    document.body.innerHTML = html
}

//DELETE ITEM
async function deleteitem(id){
    const res = await fetch(`http://127.0.0.1:5000/items/${id}` ,{
        method: "DELETE",
    })
    const html = await res.text()
    document.body.innerHTML = html

}

