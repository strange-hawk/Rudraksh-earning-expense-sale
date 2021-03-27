
const searchField = document.getElementById('searchField')
const tableOutput = document.querySelector('.table-output')
const appTable = document.querySelector('.app-table')
const tableBody = document.querySelector('.table-body')
const dateButton = document.querySelector('#dateSubmit')
const startDateField = document.querySelector('#startDateField')
const endDateField = document.querySelector('#endDateField')

tableOutput.style.display = 'none'
 
searchField.addEventListener('keyup', (e)=>{
    const searchValue = e.target.value
    if(searchValue.trim().length > 0){
        tableBody.innerHTML = ""
        tableOutput.style.display = 'none'
        appTable.style.display = 'block'
        fetch("/expense/search-expenses", {
            body : JSON.stringify({ searchText : searchValue}),
            method : 'POST'
        })
        .then(res => res.json())
        .then(data => {
            appTable.style.display = 'none'
            tableOutput.style.display = 'block'
            if(data.length === 0){
                tableBody.innerHTML = '<p>No result</p>'
            }
            else{
                data.forEach(item => {
                    tableBody.innerHTML += `
                    <tr>
                    <td>${item.name}</td>
                    <td>${item.amount}</td>
                    <td>${item.purpose}</td>
                    <td>${item.date}</td>
                    <td>${item.area}</td>
                    <td>
                    <a href="/expense/edit-expense/${item.id}" class="btn btn-primary btn-sm px-3">Edit</a>
                    <a class="btn btn-lg btn-danger btn-sm delete_modal confirm-delete" href="/expense/delete-expense/${item.id}" data-toggle="modal" data-target="#confirmDeleteModal" id="confirmDeleteModal${item.id}">Delete</a>
                </td>
                    </tr>`
                })
            }
        })
    }
    else{
        appTable.style.display = 'block'
        tableOutput.style.display = 'none'
    }
})

dateButton.addEventListener('click', (e)=>{
    const searchValue = searchField.value
    const startDate = startDateField.value
    const endDate = endDateField.value
    if(searchValue.trim().length > 0 || startDate || endDate){
        tableBody.innerHTML = ""
        tableOutput.style.display = 'none'
        appTable.style.display = 'block'
        fetch("/expense/search-expenses", {
            body : JSON.stringify({ searchText : searchValue, startDate: startDate, endDate: endDate} ),
            method : 'POST'
        })
        .then(res => res.json())
        .then(data => {
            appTable.style.display = 'none'
            tableOutput.style.display = 'block'
            if(data.length === 0){
                tableBody.innerHTML = '<p>No result</p>'
            }
            else{
                data.forEach(item => {

                    tableBody.innerHTML += `
                    <tr>
                    <td>${item.name}</td>
                    <td>${item.amount}</td>
                    <td>${item.purpose}</td>
                    <td>${item.date}</td>
                    <td>${item.area}</td>
                    <td>
                    <a href="/expense/edit-expense/${item.id}" class="btn btn-primary btn-sm px-3">Edit</a>
                    <a class="btn btn-lg btn-danger btn-sm delete_modal confirm-delete" href="/expense/delete-expense/${item.id}" data-toggle="modal" data-target="#confirmDeleteModal" id="confirmDeleteModal${item.id}">Delete</a>
                </td>
                    </tr>`
                })
            }
        })
    }
    else{
        appTable.style.display = 'block'
        tableOutput.style.display = 'none'
    }
})