/**
 * Created by wushuyi on 15-7-1.
 */

var $el = {};
var cache = {
    message: ''
};
var ajax = {};
var socket;


ajax.login = function (opt) {
    var ajax = $.ajax({
        type: "POST",
        url: "/login",
        data: {
            name: opt.name,
            room: opt.room
        }
    });
    return ajax;
};

$el.doc = $(document);
$el.win = $(window);

$el.page1 = $('#page1');
$el.userInput = $('#user');
$el.roomInput = $('#room');
$el.subinfoBtn = $('.btn', $el.page1);

$el.page2 = $('#page2');
$el.roomName = $('.room_name', $el.page2);
$el.chat = $('#chat');
$el.textInput = $('#text');
$el.submsgBtn = $('.btn-primary', $el.page2);
$el.exitBtn = $('.btn-warning', $el.page2);

$el.subinfoBtn.on('click', function (evt) {
    evt.preventDefault();
    var data = {
        name: $el.userInput.val(),
        room: $el.roomInput.val()
    };
    $el.roomName.text(data.room);
    var promise = ajax.login(data);
    promise.then(function (data) {
        if (data.data.status === 'success') {
            socket_conn();
        } else {
            alert('服务器异常!');
        }
    });
});

$el.submsgBtn.on('click', function (evt) {
    evt.preventDefault();
    var data = {
        msg: $el.textInput.val()
    };
    $el.textInput.val('');
    socket.emit('text', data);
});

$el.submsgBtn.on('keypress', function (evt) {
    var code = evt.keyCode || evt.which;
    if (code == 13) {
        var data = {
            msg: $el.textInput.val()
        };
        $el.textInput.val('');
        socket.emit('text', data);
    }
});

$el.exitBtn.on('click', function (evt) {
    evt.preventDefault();
    socket.emit('left', {});
    $el.page2.hide();
});

var socket_conn = function () {
    socket = io.connect('/chat');
    socket.on('connect', function () {
        $el.page1.hide();
        $el.page2.show();
        socket_onconnect();
    });
};

var socket_onconnect = function () {
    socket.on('status', function (data) {
        cache.message += data.msg + '\n';
        $el.chat.text(cache.message);
    });
    socket.on('message', function (data) {
        cache.message += data.msg + '\n';
        $el.chat.text(cache.message);
    });
    socket.emit('joined', {});
};