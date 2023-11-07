<template>
  <div class="post-zoom">
    <div class="container bootstrap snippets bootdey" style="height: 100vh">
      <div class="col-md-12">
        <div class="box box-widget">
          <div class="box-image">
            <div class="box-body" style="display: block">
              <h4>{{ title }}</h4>
              <img class="img-responsive pad" :src="image" alt="Photo" />
              <p>{{ description }}</p>
              <div class="tag pixel-color" v-for="(tag, index) in this.tags" :key="index">
                <p>#{{ tag }}</p>
              </div>
            </div>
          </div>
          <div class="box-info">
            <div class="box-header with-border">
              <div class="user-block">
                <img class="img-circle" :src="postAuthorProfilePic" alt="User Image" />
                <span class="username">
                {{ postAuthorUsername }}
                </span>
                <span class="description">Shared on {{ this.postDate }}</span>
              </div>
              <div class="box-tools">
                <button class="blue-button" :hidden="!isLoggedUsersPost" @click="deletePost">
                  Delete
                </button>
                <button type="button" class="blue-button" @click="redirectToMainPage()">
                  <i class="fa fa-share"></i> Go Back
                </button>
              </div>
            </div>
            <div class="box-footer box-comments" style="display: block">
              <div v-for="comment in this.comments" :key="comment.id">
                <div class="box-comment">
                  <img class="img-circle img-sm" :src="comment.image" alt="User Image" />
                  <div class="comment-text">
                    <span class="username">{{ comment.username }}
                      <span class="text-muted pull-right"> {{
                        comment.date
                      }}</span> </span>{{ comment.content }}
                  </div>
                </div>
              </div>
            </div>
            <button type="button" class="btn btn-default btn-xs">
              <span class="material-icons pixel-color full-width">favorite_border</span>
            </button>
            <span class="pull-right text-muted">127</span>
            <button type="button" class="btn btn-default btn-xs" @click="this.redirectComment()">
              <span class="material-icons pixel-color full-width">chat_bubble_outline</span>
            </button>
            <span class="pull-right text-muted">{{ this.numComments }}</span>
            <button type="button" class="btn btn-default btn-xs">
              <span class="material-icons pixel-color full-width">ios_share</span>
            </button>
            <button type="button" class="btn btn-default btn-xs bookmark">
              <span class="material-icons pixel-color full-width">bookmark</span>
            </button>
            <div class="box-footer">
              <img class="img-responsive img-circle img-sm footer-image" :src="this.loggedInUserPFP" alt="Alt Text" />
              <div class="footer-text">
                <input ref="input_comment" type="text" class="form-control input-sm" placeholder="Add a comment..."
                  maxlength="150" v-model="this.comment" @input="checkCommentSize" />
              </div>
              <button class="footer-button pixel-color" type="button" @click="this.postComment">
                Post
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { storage } from "@/firebase";
import {
  ref as firebaseRef,
  getDownloadURL,
  deleteObject,
} from "firebase/storage";

export default {
  name: "PostZoom",
  data() {
    return {
      id: this.$route.params.id,
      tags: [],
      comment: '',
      loggedInUsername: this.$route.query.loggedUsername,
      loggedInUserId: this.$route.query.loggedUserId,
      loggedInUserPFP: "",
      postAuthorProfilePic: "",
      image: "",
      title: "",
      postAuthorUsername: "",
      postDate: "",
      isLoggedUsersPost: false,
      imageFirebaseURL: "",
      description: "",
      token: this.$route.query.token,
      comments: [],
    };
  },
  computed: {
    numComments() {
      return this.comments.length;
    },
  },
  methods: {
    redirectToMainPage() {
      history.back();
    },
    checkCommentSize() {
      if (this.comment.length >= 150) {
        alert("You've reached the maximum of 150 characters for your comment.");
      }
    },
    deletePost() {
      // Ask for confirmation
      if (confirm("Are you sure you want to delete this post?")) {
        console.log("DELETING Post...");
        const postImageRef = firebaseRef(
          storage,
          "postedImages/" + this.imageFirebaseURL
        );
        const pathDelete = this.backendPath + "/publicacion/" + this.id;
        const headers = { Authorization: "Bearer " + this.token };
        axios
          .delete(pathDelete, { headers })
          .then((response) => {
            deleteObject(postImageRef)
              .then(() => {
                alert(
                  "Post with Title:" +
                  response.data.titulo +
                  " deleted successfully"
                );
                this.redirectToMainPage();
              })
              .catch((error) => {
                alert("Firebase Error: " + error.message);
              });
          })
          .catch((error) => {
            alert("Backend Error: " + error.message);
          });
      }
    },
    redirectComment() {
      this.$refs.input_comment.focus();
    },
    getPostAuthorInfo(userID) {
      const postAuthorPath = this.backendPath + "/usuario/" + userID;
      const headers = { Authorization: "Bearer " + this.token };

      axios
        .get(postAuthorPath, { headers })
        .then((response) => {
          const authorProfilePicRef = firebaseRef(
            storage,
            response.data.imagen_perfil_url
          );

          getDownloadURL(authorProfilePicRef)
            .then((url) => {
              this.postAuthorProfilePic = url;
            })
            .catch((error) => {
              alert("Firebase Error: " + error.message);
            });
        })
        .catch((error) => {
          alert("Backend Error: " + error.message);
        });
    },
    postComment() {
      const path = this.backendPath + "/comentarios";
      const headers = { Authorization: "Bearer " + this.token };
      axios.post(path, {
        "usuario_id": this.loggedInUserId,
        "publicacion_id": this.id,
        "contenido": this.comment
      }, { headers }
      ).then(() => {
        this.getComments();
      }).catch((error) => {
        alert("Error: " + error.message);
      });
    },
    getUserData(idx) {
      const path = this.backendPath + "/usuario/" + this.comments[idx].user_id;
      axios.get(path).then((res) => {
        this.comments[idx].username = res.data.nombre;
        const postImageRef = firebaseRef(
          storage,
          res.data.imagen_perfil_url);
        getDownloadURL(postImageRef)
          .then((url) => {
            this.comments[idx].image = url;
          })
          .catch((error) => {
            console.error("Firebase Error: " + error.message);
          });
      })
        .catch((error) => {
          alert("Backend Error:" + error.message);
        });
    },
    getUsersData() {
      for (let i = 0; i < this.comments.length; i += 1) {
        this.getUserData(i);
      }
    },
    getComments() {
      this.comments = []
      const path = this.backendPath + "/publicaciones/" + this.id + "/comentarios/";
      axios.get(path)
        .then((res) => {
          var comments = res.data;
          for (let i = 0; i < comments.length; i += 1) {
            const comment = {
              user_id: comments[i].usuario_id,
              post_id: comments[i].publicacion_id,
              content: comments[i].contenido,
              id: comments[i].id,
              date: new Date(comments[i].fecha_creacion).toLocaleString(),
            }
            this.comments.push(comment);
          }
          this.getUsersData();
        }).catch((error) => {
          alert("Error: " + error.message);
        });
    }
  },
  created() {
    const pathPost = this.backendPath + "/publicaciones/" + this.id;
    axios
      .get(pathPost)
      .then((response) => {
        this.title = response.data.titulo;
        this.postAuthorUsername = response.data.usuario_nombre;
        this.description = response.data.descripcion;
        this.imageFirebaseURL = response.data.imagen_url;
        this.postDate = new Date(response.data.fecha_creacion).toLocaleString();
        this.tags = JSON.parse(response.data.tags);
        if (this.loggedInUsername == this.postAuthorUsername) {
          this.isLoggedUsersPost = true;
        }
        //GETTING POST IMAGE FROM FIREBASE
        const postImageRef = firebaseRef(
          storage,
          "postedImages/" + this.imageFirebaseURL
        );
        getDownloadURL(postImageRef)
          .then((url) => {
            this.image = url;
            this.getPostAuthorInfo(response.data.usuario_id);
          })
          .catch((error) => {
            alert("Firebase Error: " + error.message);
          });
      })
      .catch((error) => {
        alert("Backend Error:" + error.message);
      });
    this.getComments();
  },
};
</script>

<style scoped>
body {
  margin-top: 20px;
  background-color: #ecf0f5;
}

.box-widget {
  border: none;
  position: relative;
}

.img-responsive {
  display: block;
  max-width: 100%;
  height: 80vh;
}

.box {
  border-radius: 3px;
  height: 100vh;
  background: #ffffff;
  border-top: 3px solid #d2d6de;
  margin-bottom: 20px;
  width: 100%;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
  display: grid;
  grid-template-columns: 60% 40%;
  grid-template-rows: auto;
  grid-gap: 0;
  /* Espacio entre las columnas (opcional) */
}

.box-header.with-border {
  border-bottom: 1px solid #f4f4f4;
}

.box-header {
  color: #444;
  display: block;
  padding: 10px;
  position: relative;
}

.user-block img {
  width: 40px;
  height: 40px;
  float: left;
}

.user-block .username {
  font-size: 16px;
  font-weight: 600;
}

.user-block .description {
  color: #999;
  font-size: 13px;
}

.user-block .username,
.user-block .description,
.user-block .comment {
  display: block;
  margin-left: 50px;
}

.box-header>.box-tools {
  position: absolute;
  right: 10px;
  top: 5px;
}

.btn-box-tool {
  padding: 5px;
  font-size: 12px;
  background: transparent;
  color: #97a0b3;
}

.box-body {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
  border-bottom-right-radius: 3px;
  border-bottom-left-radius: 3px;
  padding: 10px;
}

.pad {
  padding: 10px;
}

.box .btn-default {
  background-color: transparent;
  color: #444;
  border-color: transparent;
}

.box-footer {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
  border-bottom-right-radius: 3px;
  border-bottom-left-radius: 3px;
  border-top: 1px solid #f4f4f4;
  padding: 10px;
  background-color: #fff;
}

.box-comments .box-comment:first-of-type {
  padding-top: 0;
}

.box-comments .box-comment {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.box-comments {
  height: 70vh;
  max-height: 70vh;
  overflow-y: auto;
  background: transparent;
  border-bottom: 2px solid #eee;
}

.img-sm,
.box-comments .box-comment img,
.user-block.user-block-sm img {
  width: 30px !important;
  height: 30px !important;
}

.img-sm,
.img-md,
.img-lg,
.box-comments .box-comment img,
.user-block.user-block-sm img {
  float: left;
}

.box-comments .comment-text {
  margin-left: 40px;
  color: #555;
}

.box-comments .username {
  color: #444;
  display: block;
  font-weight: 600;
}

.box-comments .text-muted {
  font-weight: 400;
  font-size: 12px;
}

.img-sm+.img-push {
  margin-left: 40px;
}

.box .form-control {
  border-radius: 0;
  box-shadow: none;
  border-color: #d2d6de;
}

.box-info {
  grid-row: 1;
}

.box-image {
  grid-row: 1;
}

.full-width {
  display: block;
  width: 100%;
  font-size: 32px;
}

@media (max-width: 900px) {
  .box {
    grid-template-columns: 1fr;
  }

  .box-info {
    grid-row: 2;
  }

  .box-comments {
    height: auto;
    max-height: 70vh;
  }
}

.img-circle {
  border-radius: 50%;
}

.box-footer {
  display: grid;
  grid-template-columns: 10% 80% 10%;
  grid-template-rows: auto;
  grid-gap: 0;
  /* Espacio entre las columnas (opcional) */
}

.blue-button {
  background-color: rgba(20, 117, 236, 0.9);
  color: white;
  height: 30px;
  width: 5rem;
  margin: 3px;
  border-radius: 6px;
}

.blue-button.disabled-button {
  background-color: rgba(20, 117, 236, 0.5);
  pointer-events: none;
  cursor: not-allowed;
}

.blue-button:hover {
  background-color: rgba(20, 117, 236, 1);
}

.footer-text {
  grid-row: 1;
}

.footer-image {
  grid-row: 1;
}

.footer-button {
  grid-row: 1;
  font-weight: bold;
  background: transparent;
  border-color: transparent;
  transition: color 0.2s;
}

.pixel-color:hover {
  color: rgba(20, 117, 236, 0.6);
}

.pixel-color {
  color: rgba(20, 117, 236, 0.9);
}

.tag {
  display: inline-block;
  margin-right: 10px;
}

.bookmark {
  float: right;
}
</style>
