// set start and end time to be after current time
const startTime = document.querySelector('#datetime_start')
if (startTime) {
    startTime.min = new Date().toISOString().substring(0,16);
}
const endTime = document.querySelector('#datetime_end')
if (endTime) {endTime.min = new Date().toISOString().substring(0,16); }

// retrieve available reservations by sending AJAX request to sever
$('#schedule').on('submit', (evt) => {
    evt.preventDefault();

    const formData = {
        "startTime": $('[name="start_time"]').val(),
        "endTime": $('[name="end_time"]').val()
    };

    $.get("/search_reservations", formData, (res) => {
         if (res.length === 0) {
            $('#available_reservations').html("Sorry, there is no availability at these times, try another search :(")
         }
         else {
            $('#available_reservations').html("Below is the current availability. Select a time that works for you!");
            for (time of res) {
                $('#available_reservations').append(
                    `<form action="/reservations/book" method="POST">
                    <input value="${time}" name='start_time' type='submit' class='schedule_res'>
                    </form>`);
            }
         }
    })

})

// delete reservation with an AJAX request
$('.delete').on('submit', (evt) => {
    evt.preventDefault();

    const formData = {
        "startTime": $('[name="start_time"]').val()
    };

    // remove the HTML element
    $(`#${evt.target.id}`).remove();

    // remove the reservation from the database
    $.post("/reservations/delete", formData)

})