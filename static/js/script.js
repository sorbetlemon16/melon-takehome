$('#schedule').on('submit', (evt) => {
    evt.preventDefault();

    const formData = {
        "startTime": $('[name="start_time"]').val(),
        "endTime": $('[name="end_time"]').val()
    };

    $.post("/search_reservations", formData, (res) => {
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

$('.delete').on('submit', (evt) => {
    evt.preventDefault();

    const formData = {
        "startTime": $('[name="start_time"]').val()
    };

    $.post("/reservations/delete", formData, (res) => {
        $(`#${res}`).remove();
    })

})