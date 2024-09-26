export async function addFAQ(section, FAQListe) {
    let i = 1
    console.log()
    FAQListe.forEach((item) => {

        const li = document.createElement("li")
        const h2 = document.createElement("h2")
        h2.classList.add('question')
        h2.id = 'question_' + i
        h2.innerText = item.question

        const downIcon = document.createElement('span')
        downIcon.classList.add('float-end', 'faq-down')
        downIcon.innerHTML = '<i class="fa-solid fa-chevron-down"></i>'

        const upIcon = document.createElement('span')
        upIcon.classList.add('float-end', 'faq-up', 'd-none')
        upIcon.innerHTML = '<i class="fa-solid fa-chevron-up"></i>'

        h2.appendChild(downIcon);
        h2.appendChild(upIcon);

        const p = document.createElement('p')
        p.classList.add('answer')
        p.id = 'answer_' + i
        p.innerText = item.answer

        li.appendChild(h2)
        li.appendChild(p)

        section.querySelector('ul').appendChild(li)

        i = i + 1
    })
}

