console.log("Load employee delete js")

const modalBtns = [...document.getElementsByClassName("modal-button")]  // Array of buttons
const modalBody = document.getElementById("modal-body-confirm")  // body modal
const deleteBtn = document.getElementById("delete-button")  // button in modal

const current_url = window.location.href


// fill up modal info with confirm employee delete
modalBtns.forEach(modalBtn=> modalBtn.addEventListener("click", ()=>{
    const company_slug = modalBtn.getAttribute("data-company-slug")
    const employee_pk = modalBtn.getAttribute("data-employee-pk")
    const company_name = modalBtn.getAttribute("data-company-name")
    const full_name = modalBtn.getAttribute("data-employee-full-name")

    modalBody.innerHTML = `
        <div class="ht mb-3">Вы уверены что хотите удалить сотрудника "<b>${full_name}</b>"
            из субъекта "<b>${company_name}</b>"</div>
    `

    // Установить employee_pk и company_slug в атрибут deleteBtn
    deleteBtn.setAttribute("data-company-slug", company_slug)
    deleteBtn.setAttribute("data-employee-pk", employee_pk)
}))

// extract csrf token
const csrf = document.getElementsByName("csrfmiddlewaretoken")

// If delete button click
deleteEmployee = () =>{
    // extract company_slug and employee_pk from delete button
    const company_slug = deleteBtn.getAttribute("data-company-slug")
    const employee_pk = deleteBtn.getAttribute("data-employee-pk")

    // find card of deleting employee
    const employee_card = document.getElementById(`${employee_pk}`)

    $.ajax({
        type: "POST",
        url: `${current_url}employees/${employee_pk}/delete/`,
        data: {"slug": company_slug, "pk": employee_pk, "csrfmiddlewaretoken": csrf[0].value},
        success: function(response){
            employee_card.remove()  // Delete employee card from template
            console.log("Employee removed successfully")
            $("#employeeDeleteModal").modal("hide")  // close the modal
        },
        error: function(error){
        console.log(error)
        }
    })
}

deleteBtn.addEventListener("click", ()=>{
    deleteEmployee()
})