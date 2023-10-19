<template>
  <div class="post-zoom">
    <div class="container bootstrap snippets bootdey">
      <div class="col-md-8">
        <div class="box box-widget">
          <div class="box-header with-border">
            <div class="user-block">
              <img
                class="img-circle"
                src="https://bootdey.com/img/Content/avatar/avatar1.png"
                alt="User Image"
              />
              <span class="username"
                ><a href="#">{{ postAuthorUsername }}</a></span
              >
              <span class="description">Shared publicly - 7:30 PM Today</span>
            </div>
            <div class="box-tools">
              <button
                type="button"
                class="btn btn-default btn-xs"
                @click="redirectToMainPage()"
              >
                <i class="fa fa-share"></i> Go Back
              </button>
            </div>
          </div>

          <div class="box-body" style="display: block">
            <p>{{ title }}</p>
            <img class="img-responsive pad" :src="image" alt="Photo" />
            <p>{{ description }}</p>
            <button type="button" class="btn btn-default btn-xs">
              <i class="fa fa-share"></i> Share
            </button>
            <button type="button" class="btn btn-default btn-xs">
              <i class="fa fa-thumbs-o-up"></i> Like
            </button>
            <span class="pull-right text-muted">127 likes - 3 comments</span>
          </div>
          <div class="box-footer box-comments" style="display: block">
            <div class="box-comment">
              <img
                class="img-circle img-sm"
                src="https://bootdey.com/img/Content/avatar/avatar2.png"
                alt="User Image"
              />
              <div class="comment-text">
                <span class="username">
                  Christian
                  <span class="text-muted pull-right">8:03 PM Today</span>
                </span>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua.
              </div>
            </div>

            <div class="box-comment">
              <img
                class="img-circle img-sm"
                src="https://bootdey.com/img/Content/avatar/avatar3.png"
                alt="User Image"
              />
              <div class="comment-text">
                <span class="username">
                  Carlos
                  <span class="text-muted pull-right">8:03 PM Today</span>
                </span>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua.
              </div>
            </div>
          </div>
          <div class="box-footer" style="display: block">
            <form action="#" method="post">
              <img
                class="img-responsive img-circle img-sm"
                src="https://bootdey.com/img/Content/avatar/avatar1.png"
                alt="Alt Text"
              />
              <div class="img-push">
                <input
                  type="text"
                  class="form-control input-sm"
                  placeholder="Press enter to post comment"
                  :value="loggedInUsername"
                />
              </div>
            </form>
          </div>
        </div>
      </div>
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
      backendPath: "https://pixelportal-backend-api.onrender.com",
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
  height: auto;
}
.box {
  position: relative;
  border-radius: 3px;
  background: #ffffff;
  border-top: 3px solid #d2d6de;
  margin-bottom: 20px;
  width: 100%;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
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

.box-header > .box-tools {
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
  background-color: #f4f4f4;
  color: #444;
  border-color: #ddd;
}

.box-comments {
  background: #f7f7f7 !important;
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

.img-sm + .img-push {
  margin-left: 40px;
}

.box .form-control {
  border-radius: 0;
  box-shadow: none;
  border-color: #d2d6de;
}
</style>
