<template>
  <v-app>
    <v-content>
      <v-card max-width="600" class="mx-auto" outlined>
        <v-toolbar color="blue-grey" dark>
          <v-toolbar-title>{{ $route.meta.title }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon v-if="$route.name === 'splits'" @click="goto('createsplit')">
            <v-icon>mdi-credit-card-plus-outline</v-icon>
          </v-btn>
          <v-btn icon v-if="$route.name === 'splits'" @click="goto('contacts')">
            <v-icon>mdi-account-group</v-icon>
          </v-btn>
          <v-btn icon v-if="$route.name === 'splits'" @click="go">
            <v-icon>mdi-refresh</v-icon>
          </v-btn>
          <v-btn icon v-if="$route.name === 'contacts'" @click="goto('createcontact')">
            <v-icon>mdi-account-plus</v-icon>
          </v-btn>
          <v-btn icon v-if="$route.name !== 'splits'" @click="goto('splits')">
            <v-icon>mdi-home</v-icon>
          </v-btn>
          <v-btn icon v-if="$route.name !== 'splits'" @click="go(-1)">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
        </v-toolbar>
        <router-view/>
      </v-card>
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data: () => ({
  }),
  methods: {
    goto (name) {
      this.$router.push({ name })
    },
    go (num) {
      if (num) {
        this.$router.go(-1)
      } else {
        this.$router.go()
      }
    }
  }
}
</script>

<style>
  .theme--light.v-application {
    background: #fff !important;
  }
  .v-card--outlined,
  .theme--light.v-card.v-card--outlined {
    border: none !important;
  }
</style>
