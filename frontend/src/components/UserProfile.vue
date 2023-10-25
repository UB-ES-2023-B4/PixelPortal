<template>
    <div class="main-container">
        <div class="left-sidebar">
            <div class="inner">
                <div class="user-profile">
                    <div class="user-background"></div>
                    <div class="user-image">
                        <img src="https://gravatar.com/avatar/de84db04b0c7b43efdc840391ffe56ff">
                    </div>
                    <div class="user-info">
                        <p class="user-name">Daniela Desira</p>
                        <p class="user-title">Front End Developer</p>
                        <p class="user-location">
                            <i class="icon ion-md-locate"></i> Malta
                        </p>
                    </div>
                </div>
                <div class="main-menu"></div>
                <div class="social-links">
                    <a href="#"><i class="icon ion-logo-facebook"></i></a>
                    <a href="#"><i class="icon ion-logo-twitter"></i></a>
                    <a href="#"><i class="icon ion-logo-instagram"></i></a>
                </div>
            </div>
            <div class="toggle-button"><i class="icon ion-md-arrow-dropleft"></i></div>
        </div>
        <div class="main-content">

        </div>
        <div class="right-sidebar">
            <div class="btn open-music-btn"><i class="icon ion-md-musical-notes"></i></div>
            <div class="btn open-timer-btn"><i class="icon ion-md-timer"></i></div>
            <div class="btn open-chat-btn"><i class="icon ion-md-chatbubbles"></i></div>
        </div>
    </div>
</template>
  
<script>
import axios from "axios";
import { storage } from "@/firebase";
import { ref as firebaseRef, getDownloadURL } from "firebase/storage";

export default {
    name: "PostZoom",
    data() {
        return {
            id: this.$route.params.id,
            loggedInUsername: this.$route.query.loggedUsername,
            image: "",
            title: "",
            postAuthorUsername: "",
            description: "",
            token: this.$route.query.token,
        };
    },
    methods: {
        redirectToMainPage() {
            history.back();
        },
    },
    created() {
        const pathPost = this.backendPath + "/publicaciones/" + this.id;
        axios.get(pathPost).then((response) => {
            this.title = response.data.titulo;
            this.postAuthorUsername = response.data.usuario_nombre;
            this.description = response.data.descripcion;
            const postImageRef = firebaseRef(
                storage,
                "postedImages/" + response.data.imagen_url
            );
            getDownloadURL(postImageRef).then((url) => {
                this.image = url;
            });
        });
    },
};
</script>
  
<style scoped>
@import url('https://fonts.googleapis.com/css?family=Maven+Pro|Oswald');

:root {
    --border-color: #1a233d;
    --animation-duration: 0.5s;
}

* {
    box-sizing: border-box;
}

body {
    background: #0a1022;
    padding: 0;
    margin: 0;
    color: #fff;
    overflow: hidden;
    font-family: "Maven Pro";
}

.main-container {
    width: 100vw;
    height: 100vh;
    display: flex;
    overflow: hidden;
}

.main-container .left-sidebar {
    flex-grow: 2;
    max-width: 320px;
    border-right: 1px solid var(--border-color);
    position: relative;
    transition: all var(--animation-duration);
    box-shadow: 2px 0px 5px #03050a;
}

.main-container .left-sidebar .inner {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.main-container .left-sidebar .inner .user-profile {
    flex-grow: 2;
    max-height: 345px;
    display: flex;
    flex-direction: column;
    align-items: center;
    transition: all var(--animation-duration);
    border: var(--border-color);
    position: relative;
    overflow: hidden;
}

.main-container .left-sidebar .inner .user-profile .user-background {
    position: absolute;
    background: url('https://gravatar.com/avatar/de84db04b0c7b43efdc840391ffe56ff');
    background-size: cover;
    width: 100%;
    height: 100%;
    filter: blur(25px);
    z-index: -1;
}

.main-container .left-sidebar .inner .user-profile .user-background::after {
    display: block;
    position: relative;
    background-image: linear-gradient(to bottom, rgba(23, 32, 61, 0.3) 0, #0a1022 95%);
    height: 100%;
    width: 100%;
    content: '';
}

.main-container .left-sidebar .inner .user-profile .user-image {
    margin: 50px 0 25px 0;
    border-color: var(--border-color);
}

.main-container .left-sidebar .inner .user-profile .user-image img {
    width: 90px;
    border-radius: 50%;
    border: 6px solid rgba(255, 255, 255, 0.1);
}

.main-container .left-sidebar .inner .user-profile .user-info {
    text-align: center;
}

.main-container .left-sidebar .inner .user-profile .user-info .user-name {
    font-family: 'Oswald';
    font-weight: 400;
    text-transform: uppercase;
}

.main-container .left-sidebar .inner .user-profile .user-info .user-location {
    color: #D1D3DA;
}

.main-container .left-sidebar .inner .user-profile .user-info i::before {
    transform: rotate(180deg);
    color: #556798;
}

.main-container .left-sidebar .inner .main-menu {
    flex-grow: 5;
}

.main-container .left-sidebar .inner .social-links {
    flex-grow: 1;
    max-height: 50px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
}

.main-container .left-sidebar .inner .social-links a {
    padding: 0 10px;
    color: #fff;
    font-size: 1.3rem;
}

.main-container.minimize .left-sidebar {
    max-width: 100px;
}

.main-container.minimize .left-sidebar .inner .user-profile {
    border-bottom: 1px solid #1a233d;
    max-height: 130px;
}

.main-container.minimize .left-sidebar .inner .user-profile .user-image {
    margin: 25px 0;
}

.main-container.minimize .left-sidebar .inner .user-profile .user-image img {
    width: 75px;
}

.main-container.minimize .left-sidebar .inner .user-profile .user-info {
    height: 0px;
    transition-delay: 0s;
    animation: animate-sidebar-text var(--animation-duration);
}

.main-container.minimize .left-sidebar .inner .social-links {
    max-height: 200px;
    flex-direction: column;
}

.main-container.minimize .left-sidebar .inner .social-links a {
    padding: 10px 0;
}

.main-container.minimize .left-sidebar .toggle-button i::before {
    transform: rotate(180deg);
}

.main-container .main-content {
    flex-grow: 10;
    display: flex;
    justify-content: center;
}

.main-container .main-content>div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.main-container .main-content .modal {
    border: 1px solid var(--border-color);
    padding: 0 20px;
    width: 50%;
    border-radius: 25px;
    display: none;
}

.main-container .main-content .modal.show {
    display: inherit;
}

.main-container .main-content .modal .heading h2 {
    font-size: 1.3rem;
    padding: 10px 0;
    letter-spacing: 0.1rem;
    font-weight: 400;
}

.main-container .main-content .modal .heading h3 {
    letter-spacing: -0.03rem;
    font-family: 'Oswald';
    text-transform: uppercase;
}

.main-container .right-sidebar {
    flex-grow: 1;
    max-width: 100px;
    border-left: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}

.main-container .right-sidebar .btn {
    border-top: 1px solid var(--border-color);
    height: 50px;
    line-height: 50px;
    width: 100%;
    text-align: center;
    cursor: pointer;
}

.toggle-button {
    position: absolute;
    top: 50%;
    left: 100%;
    border: 1px solid #1a233d;
    width: 25px;
    height: 100px;
    text-align: center;
    line-height: 100px;
    border-radius: 0 50% 50% 0;
    cursor: pointer;
    transform: translate(0, -50%);
    box-shadow: 2px 0px 5px #03050a;
    background: #0a1022;
    z-index: 1;
}

.toggle-button:hover {
    background: var(--border-color);
}

.toggle-button i::before {
    transition: all var(--animation-duration) / 2;
}

@keyframes animate-sidebar-text {
    0% {}

    100% {
        opacity: 0;
        margin-top: -5px;
    }
}

.main-content {
    padding: 50px;
    position: relative;
}

.audio-player-large {
    background: #101734;
    width: 250px;
    height: 305px;
    border-radius: 10px;
    overflow: hidden;
    text-align: left;
    margin-bottom: 20px;
}

.audio-player-large .audio-image {
    width: 100%;
    height: 250px;
    background: url('https://www.atelevisao.com/wp-content/uploads/2018/02/Imagine-Dragons-642x556.jpg') center center;
    background-size: cover;
    padding: 20px;
    text-transform: uppercase;
}

.audio-player-large .audio-image .artist-name {
    letter-spacing: -0.03rem;
}

.audio-player-large .audio-image .song-title {
    font-size: 1.3rem;
    padding: 10px 0;
    border-bottom: 1px solid #fff;
    border-radius: 2px;
    letter-spacing: 0.1rem;
}

.audio-player-large .audio-slider {
    width: 100%;
    height: 5px;
    background: #101734;
}

.audio-player-large .audio-slider .slider {
    background: #2f8fff;
    width: 25%;
    height: 100%;
}

.audio-player-large .audio-buttons {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50px;
    border-top: 1px solid var(--border-color);
}

.audio-player-large .audio-buttons>div {
    flex-grow: 1;
    text-align: center;
    line-height: 50px;
    cursor: pointer;
}

.audio-player-large .audio-buttons>div:hover {
    background: var(--border-color);
    box-shadow: inset 0px 0px 5px #03050a;
}

.audio-player-large .audio-buttons>div:nth-child(2) {
    border-left: 1px solid var(--border-color);
    border-right: 1px solid var(--border-color);
}

.audio-player-small {
    width: 500px;
    border-radius: 10px;
    overflow: hidden;
    height: 100px;
    display: flex;
    align-items: center;
    padding: 10px;
    position: relative;
    text-align: left;
    margin-bottom: 20px;
}

.audio-player-small .audio-background {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    background: url('https://www.atelevisao.com/wp-content/uploads/2018/02/Imagine-Dragons-642x556.jpg') center center;
    z-index: -1;
}

.audio-player-small .audio-background::after {
    content: '';
    background: linear-gradient(45deg, rgba(182, 92, 118, 0.2), rgba(72, 64, 111, 1) 80%);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

.audio-player-small .audio-image {
    width: 75px;
    height: 75px;
    margin: 0 10px;
    background: url('https://www.atelevisao.com/wp-content/uploads/2018/02/Imagine-Dragons-642x556.jpg') center center;
    background-size: cover;
    border-radius: 50%;
}

.audio-player-small .audio-image::before {
    content: '';
    border: 2px solid #0d162d;
    border-top: 2px solid #2f8fff;
    border-radius: 50%;
    width: 75px;
    height: 75px;
    display: block;
    position: relative;
    transform: rotate(40deg);
}

.audio-player-small .audio-info {
    margin: 0 10px;
    flex-grow: 2;
}

.audio-player-small .audio-info .audio-text {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: -0.03rem;
}

.audio-player-small .audio-info .song-title {
    font-size: 1.3rem;
    padding: 5px 0;
    letter-spacing: 0.1rem;
}

.audio-player-small .audio-info .audio-slider {
    width: 100%;
    height: 5px;
    background: #0d162d;
    margin-top: 10px;
}

.audio-player-small .audio-info .audio-slider .slider {
    background: #2f8fff;
    width: 25%;
    height: 100%;
}

.audio-player-small .audio-buttons {
    display: flex;
    align-items: center;
    height: 100%;
}

.audio-player-small .audio-buttons>div {
    margin: 0 10px;
}

.direct-messaging {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 250px;
    height: 350px;
    background: black;
    margin: 0 !important;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    align-content: stretch;
    background: linear-gradient(to bottom, #080d1d 0%, #1a233d 100%);
    box-shadow: 2px 0px 5px #03050a;
    transition: all var(--animation-duration);
}

.direct-messaging.minimize {
    bottom: -350px;
}

.direct-messaging .header-container {
    display: flex;
    flex-grow: 1;
    background: #080d1d;
    max-height: 50px;
    align-items: center;
    justify-content: space-between;
    width: 100%;
}

.direct-messaging .header-container>div {
    flex-grow: 1;
    padding: 0 5px;
}

.direct-messaging .header-container img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-left: 5px;
}

.direct-messaging .header-container .header-user {
    display: flex;
    align-items: center;
    justify-content: center;
}

.direct-messaging .header-container .header-user .online {
    padding: 5px;
    border-radius: 50%;
    background: green;
    margin-left: 10px;
    height: 5px;
}

.direct-messaging .header-container .close-chat-btn {
    line-height: 50px;
    text-align: center;
    cursor: pointer;
}

.direct-messaging .header-container .close-chat-btn:hover {
    background: #1a233d;
}

.direct-messaging .message-container {
    flex-grow: 2;
    display: flex;
    flex-direction: column;
    padding: 5px 10px;
    overflow-y: scroll;
    max-height: 250px;
}

.direct-messaging .message-container::-webkit-scrollbar {
    width: 0px;
    background: transparent;
}

.direct-messaging .message-container .msg {
    font-size: 0.8rem;
    max-width: 90%;
    display: flex;
    flex-direction: column;
    margin: 0.5rem 0;
}

.direct-messaging .message-container .msg p {
    margin: 0.5rem 0;
}

.direct-messaging .message-container .msg .text {
    border-radius: 10px;
    padding: 5px 10px;
    margin-bottom: 5px;
    line-height: 1.2rem;
}

.direct-messaging .message-container .msg .time {
    font-size: 0.6rem;
    color: #868686;
}

.direct-messaging .message-container .msg.received {
    align-self: flex-start;
}

.direct-messaging .message-container .msg.received .text {
    background: #c2448a;
}

.direct-messaging .message-container .msg.sent {
    text-align: right;
    align-self: flex-end;
}

.direct-messaging .message-container .msg.sent .text {
    background: #413c5e;
}

.direct-messaging .send-container {
    display: flex;
    flex-grow: 1;
    background: #080d1d;
    border-top: 1px solid #1a233d;
    padding: 0 5px;
    max-height: 50px;
    width: 100%;
}

.direct-messaging .send-container input {
    background: transparent;
    border: none;
    padding: 0 5px;
    flex-grow: 3;
    color: #fff;
}

.direct-messaging .send-container input:focus {
    outline: none;
}

.direct-messaging .send-container .send-btn {
    align-self: center;
    flex-grow: 1;
    text-align: center;
    padding: 0 5px;
    background: #0c1225;
    height: 2rem;
    line-height: 2rem;
    border-radius: 50%;
    cursor: pointer;
}

.direct-messaging .send-container .send-btn:hover {
    background: #1a233d;
}

.direct-messaging .send-container .send-btn i::before {
    transform: rotate(-45deg);
}

.countdown-timer-large {
    background: url('https://images.wallpapersden.com/image/wxl-desert-nights-moon-5k-minimalism_57965.jpg');
    background-size: cover;
    background-position: 50% 100%;
    width: 400px;
    height: 305px;
    border-radius: 10px;
    overflow: hidden;
    text-align: center;
    margin-bottom: 20px;
}

.countdown-timer-large .countdown-background {
    position: absolute;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    z-index: -1;
}

.countdown-timer-large .countdown-timer {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    font-family: 'Oswald';
}

.countdown-timer-large .countdown-timer h2 {
    font-size: 2.5rem;
    color: #fff;
    margin: 0;
}

.countdown-timer-large .countdown-timer .countdown {
    display: flex;
    align-items: center;
    font-size: 1rem;
    color: #fff;
    margin: 5px 0;
}

.countdown-timer-large .countdown-timer .countdown span {
    padding: 0 5px;
}

.countdown-timer-small {
    background: url('https://images.wallpapersden.com/image/wxl-desert-nights-moon-5k-minimalism_57965.jpg');
    background-size: cover;
    background-position: 50% 100%;
    width: 250px;
    height: 100px;
    border-radius: 10px;
    overflow: hidden;
    display: flex;
    align-items: center;
    position: relative;
    text-align: center;
    margin-bottom: 20px;
}

.countdown-timer-small .countdown-background {
    position: absolute;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    z-index: -1;
}

.countdown-timer-small .countdown-timer {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: 'Oswald';
    font-size: 1.2rem;
    color: #fff;
    width: 100%;
}

.countdown-timer-small .countdown-timer .countdown {
    display: flex;
    align-items: center;
    font-size: 0.8rem;
    color: #fff;
    margin: 5px 0;
}

.countdown-timer-small .countdown-timer .countdown span {
    padding: 0 5px;
}
</style>
  