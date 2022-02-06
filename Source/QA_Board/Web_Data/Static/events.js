{
    let pub_question_list = document.getElementById("ques-pub")
    let pri_question_list = document.getElementById("ques-pri")

    document.getElementById("ShowPub").addEventListener("click", function()
        {
            pub_question_list.style.display = "block";
            pri_question_list.style.display = "none";
        }
    )

    document.getElementById("ShowPri").addEventListener("click", function()
        {
            pub_question_list.style.display = "none";
            pri_question_list.style.display = "block";
        }
    )
}
{
    course_select_buttons = document.getElementById("course").children

    for (let option = 0; option < course_select_buttons.length; option++)
    {
        course_select_buttons[option].addEventListener("click", function()
            {
                option_text = course_select_buttons[option].textContent;
                document.getElementById("course-dropdown").textContent = option_text;
                document.getElementById("selected-course").value = option_text;
            }
        )
    }
}
{
    $( document.getElementById("main-content") ).click(function() {
        $(".js-hiddenform").slideUp();
    });

    $(".js-expand").click(function() {
        if ($('#title').val()) {
              //validate form
        } else {
            $(".js-hiddenform").slideDown();
        }
    });
}