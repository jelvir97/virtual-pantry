$addIngBtn = $('#add-ing-field')
$ingField = $('.ing-field')
$wrapper = $('#ing-wrapper')
function handleAddIngField(evt){
    evt.preventDefault()
    $currField = $(evt.target).parent()
    $currField.next().show()
    $(evt.target).hide()
    
    $currField.next().children('#add-ing-field').on('click',handleAddIngField)
    $currField.next().children('#remove-ing-field').on('click',handleRemoveIngField)

    $remBtn = $('#remove-ing-field')
    $remBtn.on('click',handleRemoveIngField)
}

$addIngBtn.on('click',handleAddIngField)

function handleRemoveIngField(evt){
    evt.preventDefault()
    $currField = $(evt.target).parent()
    $inputs = $currField.find('input')
    for(i of $inputs){
        i.value = ''
    }

    $currField.prev().children('#add-ing-field').show()
    $currField.prev().children('#remove-ing-field').show()
    $currField.hide()
}