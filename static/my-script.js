class BoggleGame{

    constructor(boardId, secs=60){
        this.secs = secs;
        this.boardId = $('#' + boardId);
        this.score = 0;
        this.words = [];
        this.showTimer();

        this.timer = setInterval(this.countDown.bind(this), 1000);

        $('.add-word').on('submit', this.handleSubmit.bind(this));
    }


    showWord(word){
        $('.words').append($('<li>', {text: word}));
    }

    showScore(){
        $('.score').text(this.score);
    }

    async handleSubmit(e){
        e.preventDefault();
        let word = $('.word').val();

        if(!word) return;
        if(this.words.includes(word)){
            $('.msg').text(`You already guessed ${word}`);
            $('.word').val('');
            return
        }
        
        const res = await axios.get('/check-word', { params: {word: word} });
        console.log(res);
        if (res.data.result === 'not-word'){
            $('.msg').text(`${word} is not a valid English word`);
        } else if (res.data.result === 'not-on-board'){
            $('.msg').text(`${word} is not valid on this board`);
        } else {
            this.words.push(word);
            this.showWord(word);
            this.score += word.length;
            this.showScore();
            $('.msg').text(`${word} added!`)
        }
        $('.word').val('');
    }

    showTimer(){
        $('.timer').text(this.secs);
    }

    async countDown(){
        this.secs--;
        this.showTimer();

        if (this.secs === 0){
            clearInterval(this.timer);
            await this.postScore()
        }
    }

    async postScore(){
        $('.add-word').hide();
        const res = await axios.post('/post-score', { score: this.score});
        console.log(res);
        if (res.data.brokeRecord){
            $('.msg').text(`New Record: ${this.score}`);
        } else {
            $('.msg').text(`Your Score: ${this.score}`)
        }
    }
}