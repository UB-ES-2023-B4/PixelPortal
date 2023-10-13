<template>
  <transition name="fade">
    <div class="popup" v-show="open">
      <transition name="drop-in">
        <div class="popup-inner" v-show="open">
          <div class="popup-content">
            <h1>Post Image</h1>
            <h3>Preview:</h3>
            <div class="form-input">
              <img
                :src="postImagePath"
                alt=""
                class="image-preview-display"
                ref="imagePreviewDisplay"
              />
            </div>
            <div class="form-input">
              <input
                type="file"
                class="image-upload-input"
                ref="imageInput"
                accept="image/png,image/jpeg"
                @change="imageInputChanged"
              />
            </div>
            <div class="form-input">
              <input
                type="text"
                placeholder="Title"
                class="image-title-input"
                v-model="imageTitle"
              />
            </div>
            <div class="form-input">
              <textarea
                type="text"
                placeholder="Description"
                class="image-description-input"
                v-model="imageDescription"
              />
            </div>
            <div class="form-button">
              <button type="button" @click="closeComponent">Close</button>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </transition>
</template>

<script>
export default {
  name: "UploadImagePopup",
  props: {
    open: {
      type: Boolean,
      required: true,
    },
    username: {
      type: String,
      required: true,
    },
    token: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      defaultImagePath: require("@/assets/default_PFP.png"),
      postImagePath: require(`@/assets/default_PFP.png`),
      imageTitle: "",
      imageDescription: "",
    };
  },
  methods: {
    imageInputChanged() {
      const imageInput = this.$refs.imageInput;

      this.postImagePath = URL.createObjectURL(imageInput.files[0]);
    },
    closeComponent() {
      const imageInput = this.$refs.imageInput;
      this.postImagePath = this.defaultImagePath;
      imageInput.value = "";
      this.imageTitle = "";
      this.imageDescription = "";
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
*,
::before,
::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
  overflow-y: auto;
  z-index: 3;
  background-color: rgba(0, 0, 0, 0.6);
}

.popup-inner {
  max-width: 500px;
  margin: 2rem auto;
}

.popup-content {
  position: relative;
  background-color: white;
  border: 1px solid rgba(0, 0, 0, 0.3);
  background-clip: padding-box;
  border-radius: 0.3rem;
  padding: 1rem;
}

.form-input {
  margin-bottom: 10px; /* Adjust the margin as needed to separate the elements */
}

.image-preview-display {
  height: 300px;
  width: 300px;
  border-radius: 10%;
  object-fit: cover;
  background: #dfdfdf;
}

.image-title-input {
  width: 100%;
}
.image-description-input {
  height: 100px;
  resize: vertical;
  overflow-y: auto;
  padding: 5px;
  width: 100%;
}
.form-button {
  margin-top: 10px; /* Adjust the margin as needed to separate the elements */
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.drop-in-enter-active,
.drop-in-leave-active {
  transition: all 0.3s ease-out;
}

.drop-in-enter-from,
.drop-in-leave-to {
  opacity: 0;
  transform: translateY(-50px);
}
</style>
