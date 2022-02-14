{
    // Function that shows and hides the question inout form
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

{
    // Function that gets the input from any comment reply section and sends it to the hidden form
    let reply_buttons = document.getElementsByClassName("comment-submit");
    let form_text = document.getElementById("comment-text");
    let form_parent = document.getElementById("comment-parent");

    for (let button = 0; button < reply_buttons.length; button++)
    {
        reply_buttons[button].addEventListener("click", function()
            {
               let parent_id = reply_buttons[button].value;
               console.log(reply_buttons[button])
               let comment_text = document.getElementById(parent_id + "-comment");
               form_text.value = comment_text.value;
               form_parent.value = parent_id;

               document.getElementById("comment-creator").submit();
            }
        )
    }
}

{
    // function to display the course options on the question input form
    let course_select_buttons = document.getElementById("course").children;

    for (let option = 0; option < course_select_buttons.length; option++)
    {
        course_select_buttons[option].addEventListener("click", function()
            {
                let option_text = course_select_buttons[option].textContent;
                document.getElementById("course-dropdown").textContent = option_text;
                document.getElementById("selected-course").value = option_text;
            }
        )
    }
}

{
    // function that controls whether the questions shown are public or private
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
    // function that will match a search input to all the available questions being displayed
    search_bar = document.getElementById("search-bar");
    search = search_bar.value.toLowerCase();

    private_questions = document.getElementById("ques-pri").getElementsByTagName('li');
    public_questions = document.getElementById("ques-pub").getElementsByTagName('li');

    if (private_questions.length && public_questions.length)
    {

        all_questions = Array.prototype.push.apply(private_questions, public_questions)

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
}