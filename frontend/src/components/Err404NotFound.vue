<template>
  <section class="page_404">
    <div class="container">
      <div class="row">
        <div class="col-sm-12 ">
          <div class="col-sm-10 col-sm-offset-1  text-center">
            <div class="four_zero_four_bg" />
            <div class="contant_box_404">
              <v-btn
                class="link_404 "
                color="error"
                text="Покинуть страницу"
                variant="flat"
                @click="leavePage"
              >
                <template #prepend>
                  <v-icon
                    icon="mdi-home-alert-outline"
                    size="30px"
                  />
                </template>
              </v-btn>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
  import router from '@/router';

  export default {
    name: 'Err404NotFound',
    methods: {
      leavePage () {
        router.push({ name: 'login' })
      },
    },
  }
</script>

<style>
.page_404 {
  padding: 40px 0;
  background: #fff;
  font-family: 'Arvo', serif;
}

.page_404 img {
  width: 100%;
}

.four_zero_four_bg {

  background-image: url("@/assets/kGwR3uDrUKPI.gif");
  height: 400px;
  background-position: center;
}


.four_zero_four_bg h1 {
  font-size: 80px;
}

.four_zero_four_bg h3 {
  font-size: 80px;
}

.link_404 {
  margin: 20px 0;
}

.contant_box_404 {
  margin-top: -50px;
}
</style>
