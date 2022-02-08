{
    let pub_question_list = document.getElementById("ques-pub");
    let pri_question_list = document.getElementById("ques-pri");

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
    course_select_buttons = document.getElementById("course").children;

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
    search_bar = document.getElementById("search-bar");
    search = search_bar.value.toLowerCase();

    private_questions = document.getElementById("ques-pri").getElementsByTagName('li');
    public_questions = document.getElementById("ques-pub").getElementsByTagName('li');

    all_questions = private_questions.concat(public_questions);

    for (let question = 0; question < all_questions.length; question++)
    {
        title = all_questions[question].getElementsByTagName("a")[0];

        if (title.textContent.toLowerCase().indexOf(filter) > -1) {
            all_questions[question].style.display = "";
        } else {
            all_questions[question].style.display = "none";
        }
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