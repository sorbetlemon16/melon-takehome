// set start and end time to be after current time
const startTime = document.querySelector('#datetime_start')
startTime.min = new Date().toISOString().substring(0,16);
const endTime = document.querySelector('#datetime_end')
endTime.min = new Date().toISOString().substring(0,16);

// retrieve available reservations by sending AJAX request to sever
document.querySelector('#schedule').addEventListener('submit', (evt) => {
    evt.preventDefault();

    const formData = {
        "startTime": $('[name="start_time"]').val(),
        "endTime": $('[name="end_time"]').val()
    };

    const queryString = new URLSearchParams(formData).toString();

    fetch(`/search_reservations?${queryString}`)
        .then(response => response.json())
        .then(res => {
            if (res.length === 0) {
                document.getElementById('available_reservations').innerHTML 
                    = "Sorry, there is no availability at these times, try another search :(";  
            }
            else {
                document.getElementById('reservation_text').innerHTML 
                    = "Below is the current availability. Select a time that works for you!";
                for (time of res) {
                    document.getElementById('available_reservations').insertAdjacentHTML(
                        'beforeend',
                        `<form action="/reservations/book" method="POST">
                        <input value="${time}" name='start_time' type='submit' class='schedule_res'>
                        </form>`);
                }
            }
        })

})

