console.log("expense js")
const searchField = document.getElementById('searchField')
const tableOutput = document.querySelector('.table-output')
const appTable = document.querySelector('.app-table')
const tableBody = document.querySelector('.table-body')
const startDateField = document.querySelector('#startDateField')
const endDateField = document.querySelector('#endDateField')


console.log("startDateField", startDateField)
console.log("endDateField",endDateField)

tableOutput.style.display = 'none'
startDateField.addEventListener('change', (e)=>{
    const dateValue = new Date(e.value)
    console.log(dateValue)
})

searchField.addEventListener('keyup', (e)=>{
    const searchValue = e.target.value
    console.log(searchValue)
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
                    <td>${item.date}</td>
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