<template>
  <v-card max-width="600" class="mx-auto" outlined>
    <v-list three-line subheader v-if="!isFetching">
      <template v-for="(contact, $index) in contacts">
        <v-list-item :key="contact.id">
          <v-list-item-avatar>
            <v-avatar color="blue-grey" size="48">
              <span class="white--text headline">{{ contact.name[0].toUpperCase() }}</span>
            </v-avatar>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title v-text="contact.name"></v-list-item-title>
            <v-list-item-subtitle class="caption" v-text="contact.phone"></v-list-item-subtitle>
            <v-list-item-subtitle class="caption" v-text="contact.email"></v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-divider v-if="$index + 1 < contacts.length" :key="'div-' + $index"></v-divider>
      </template>
    </v-list>
    <div v-else class="fetching">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <v-dialog v-model="isFetchError" persistent max-width="290">
      <v-card v-if="isFetchError">
        <v-card-title class="headline">Error</v-card-title>
        <v-card-text>Error getting split, try again.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="fetch">Ok</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      isFetching: false,
      isFetchError: false,
      contacts: [],
      isInfo: false,
      info: {}
    }
  },
  mounted () {
    this.fetch()
  },
  methods: {
    fetch () {
      this.isFetching = true
      this.isFetchError = false
      axios.get('/api/contacts/').then((resp) => {
        let contacts = []
        for (let c of resp.data) {
          c.name = c.name[0].toUpperCase() + c.name.slice(1)
          contacts.push(c)
        }
        this.contacts = contacts
      }).catch((_) => {
        this.isFetchError = true
      }).finally(() => {
        this.isFetching = false
      })
    }
  }
}
</script>

<style>
  .v-chip {
    min-width: 110px;
  }
  .fetching {
    text-align: center;
    padding: 200px 0;
  }
  .created-at {
    font-size: 10px;
  }
  .capitalize {
    text-transform: capitalize;
  }
  .settled-contacts {
    opacity: 0.6;
  }
</style>
