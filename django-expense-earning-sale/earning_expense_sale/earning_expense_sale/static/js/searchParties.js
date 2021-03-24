const searchField = document.getElementById('searchField')
const tableOutput = document.querySelector('.table-output')
const appTable = document.querySelector('.app-table')
const tableBody = document.querySelector('.table-body')


tableOutput.style.display = 'none'

searchField.addEventListener('keyup', (e)=>{
    const searchValue = e.target.value
    console.log(searchValue)
    if(searchValue.trim().length > 0){
        tableBody.innerHTML = ""
        tableOutput.style.display = 'none'
        appTable.style.display = 'block'
        fetch("/party/search-party/", {
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
                    <td>${item.area}</td>
                    <td>${item.reference}</td>
                    <td>${item.contact}</td>
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
