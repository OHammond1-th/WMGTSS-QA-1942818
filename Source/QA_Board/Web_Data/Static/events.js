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