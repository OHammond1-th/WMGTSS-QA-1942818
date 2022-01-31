let pub_question_list = document.getElementById("ques-pub")
let pri_question_list = document.getElementById("ques-pri")

document.getElementById("ShowPub").addEventListener("click", function()
    {
        pub_question_list.style.display = "block";
        pri_question_list.style.display = "hidden";
    }
)

document.getElementById("ShowPri").addEventListener("click", function()
    {
        pub_question_list.style.display = "hidden";
        pri_question_list.style.display = "block";
    }
)