console.log("Arnaud Tadonkeng")

// collect items from the form
const itemForm = document.querySelector('#itemForm')

// add an event to the form
itemForm.addEventListener("submit", async function(event){
    event.preventDefault()
    const name = document.querySelector('#name').value
    const price = document.querySelector('#price').value

    try{
        // await pauses until the request finishes; fetch() sends an HTTP request
        const res = await fetch("/items", {
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name: name, price: Number(price)})
        })
        const data = await res.json()
        document.querySelector('#response').innerText = "Response: " + JSON.stringify(data)
        itemForm.reset()
    }
    catch(error){
        document.querySelector('#response').innerText = "Error: " + error
    }
})

// LOADING ALL ITEMS
async function loaditems(){
    const res = await fetch("/items")
    const data = await res.json()

    const list = document.querySelector('.itemslist')
    list.innerHTML = ""   // clear the list so items are not duplicated on reload

    for (const id in data){
        const item = data[id]
        const li = document.createElement('li')

        const info = document.createElement('span')
        info.className = "info"
        info.textContent = `ID ${id}: ${item.name}, $${item.price}`

        const updateBtn = document.createElement('button')
        updateBtn.textContent = "Update"
        updateBtn.addEventListener("click", () => showupdateform(id, item.name, item.price))

        const deleteBtn = document.createElement('button')
        deleteBtn.textContent = "Delete"
        deleteBtn.className = "danger"
        deleteBtn.addEventListener("click", () => deleteitem(id))

        li.append(info, updateBtn, deleteBtn)
        list.appendChild(li)
    }
}

// show the update form filled with the selected item
function showupdateform(id, name, price){
    document.querySelector("#updatesection").style.display = "block"
    document.querySelector("#updateName").value = name
    document.querySelector("#updateID").value = id
    document.querySelector("#updatePrice").value = price
}

// update the selected item's name and/or price
async function updateItem(){
    const id = document.querySelector("#updateID").value
    const name = document.querySelector("#updateName").value
    const price = document.querySelector("#updatePrice").value

    const res = await fetch(`/items/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name: name, price: Number(price)})
    })
    const html = await res.text()
    document.open()
    document.write(html)   // show update.html (keeps its CSS link)
    document.close()
}

// DELETE ITEM
async function deleteitem(id){
    const res = await fetch(`/items/${id}`, {method: "DELETE"})
    const html = await res.text()
    document.open()
    document.write(html)   // show delete.html
    document.close()
}