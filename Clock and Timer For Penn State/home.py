<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Setup Options</title>
    <style> 
        body, html{
            height: 100%;
            width: 100%;
            display:flex;
            justify-content: center;
            align-items: center;
            background-color: pink;
        }

        .event_list_color{
            position: absolute;
            top: 100px;
            background-color: papayawhip;
            width: 500px;
            height: 100%;
        }

        .event_list{
            position: absolute;
            top: 100px;
            background-color: papayawhip;
            width: 500px;
            height: auto;
            display: grid;
        }
        
        .event_add{
            gap: 20px;
            display: flex;
            position: relative;
            width: 100px;
            height: 25px;
        }

        .event_list_label{
            width: 100%;
            height: 100%;
            position: relative;
            display:grid;
            grid-template-columns: repeat(2, 300px);
            grid-template-rows: repeat(auto-fill);
        }



    </style> 
</head>

<body>
    <div class = 'event_list_color', id = 'event_list_color'>

    </div>
    <div class = 'event_list', id = 'event_list'>
        <div class = 'event_add'>
            <input type = 'text' id = 'event_add_text' placeholder='ex.brushing teeth, getting ready, eating breakfast'> 
            
            <select id = 'time_options' name = 'time_options'> 
                <option value = '' disabled selected>Select a time!</option>
                <option value = '5'>5 minutes</option>
                <option value = '10'>10 minutes</option>
                <option value = '15'>15 minutes</option>
                <option value = '20'>20 minutes</option>
                <option value = '25'>25 minutes</option>
                <option value = '30'>30 minutes</option>
                <option value = '35'>35 minutes</option>
                <option value = '40'>40 minutes</option>
                <option value = '45'>45 minutes</option>
                <option value = '50'>50 minutes</option>
                <option value = '55'>55 minutes</option>
                <option value = '60'>60 minutes</option>
            </select>

            <button id = 'enter'>Enter</button>
            
            <form id = 'time_form' action = '/time_data' method='POST'>
                <input type = 'hidden'  name = 'time' id = 'time' value = '0'>
                <input type = 'submit' value = 'submit'> 
            </form>
        </div>

        <div class = 'event_list_label' id = 'event_list_label'> 

        </div>
    </div>
    
    <script>
        document.getElementById('enter').addEventListener('click', function() {
            const event_add_text = document.getElementById('event_add_text').value;
            const time_add = document.getElementById('time_options').value;
            document.getElementById('time').value = (parseInt(document.getElementById('time').value) || 0) + (parseInt(time_add) || 0);


            if (event_add_text && time_add) {
                const new_event_label = document.createElement('label');
                const new_time_label = document.createElement('label');
                new_time_label.textContent = time_add;
                new_event_label.textContent = event_add_text;
                document.getElementById('event_list_label').appendChild(new_event_label);
                document.getElementById('event_list_label').appendChild(new_time_label);
                document.getElementById('event_add_text').value= '';
                document.getElementById('time_options').value = '';
            }
        });
    </script>
</body>
</html>
