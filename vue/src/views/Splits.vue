<template>
  <v-card max-width="600" class="mx-auto" outlined>
    <v-list two-line subheader v-if="!isFetching">
      <template v-for="(split, $index) in splits">
        <v-list-item :key="split.id" @click="showInfo(split)">
          <v-list-item-avatar>
            <v-avatar color="blue-grey" size="48">
              <span class="white--text headline">{{ split.name[0].toUpperCase() }}</span>
            </v-avatar>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title v-text="split.name"></v-list-item-title>
            <v-list-item-subtitle class="caption" v-text="split.created_at"></v-list-item-subtitle>
          </v-list-item-content>

          <v-list-item-action>
            <v-chip v-if="split.settled" class="ma-2" color="teal" text-color="white">
              <v-avatar left>
                <v-icon>mdi-checkbox-marked-circle</v-icon>
              </v-avatar>
              Settled
            </v-chip>
            <v-chip v-else class="ma-2" color="orange darken-1" text-color="white">
              <v-avatar left>
                <v-progress-circular :value="split.settlementProgress" :size="20" color="orange lighten-2"></v-progress-circular>
              </v-avatar>
              Pending
            </v-chip>
          </v-list-item-action>
        </v-list-item>
        <v-divider v-if="$index + 1 < splits.length" :key="$index"></v-divider>
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
          <v-btn color="green darken-1" text @click="fetchSplits">Ok</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <template v-if="isInfo && info">
      <v-bottom-sheet v-model="isInfo">
        <v-card max-width="600" class="mx-auto">
          <v-list subheader>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title class="capitalize" v-text="info.name"></v-list-item-title>
              </v-list-item-content>

              <v-list-item-action>
                ₹{{ info.amount }}
              </v-list-item-action>
            </v-list-item>
            <v-divider></v-divider>

            <template v-if="info.pending_contacts.length > 0">
              <v-subheader>Pending</v-subheader>
              <v-list-item v-for="item in info.pending_contacts" :key="item.name">
                <v-list-item-avatar>
                  <v-avatar color="blue-grey" size="32">
                    <span class="white--text headline">{{ item.name[0].toUpperCase() }}</span>
                  </v-avatar>
                </v-list-item-avatar>

                <v-list-item-content>
                  <v-list-item-title class="capitalize" v-text="item.name"></v-list-item-title>
                </v-list-item-content>

                <v-list-item-action>
                  ₹{{ item.amount }}
                </v-list-item-action>
              </v-list-item>
              <v-divider></v-divider>
            </template>

            <template v-if="info.settled_contacts.length > 0">
              <v-subheader>Settled</v-subheader>
              <v-list-item v-for="item in info.settled_contacts" :key="item.name" class="settled-contacts">
                <v-list-item-avatar>
                  <v-avatar color="blue-grey" size="32">
                    <span class="white--text headline">{{ item.name[0].toUpperCase() }}</span>
                  </v-avatar>
                </v-list-item-avatar>

                <v-list-item-content>
                  <v-list-item-title class="capitalize" v-text="item.name"></v-list-item-title>
                  <v-list-item-subtitle v-text="'Settled on ' + item.settlement_date"></v-list-item-subtitle>
                </v-list-item-content>

                <v-list-item-action>
                  ₹{{ item.amount }}
                </v-list-item-action>
              </v-list-item>
            </template>
          </v-list>
        </v-card>
      </v-bottom-sheet>
    </template>
  </v-card>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      isFetching: false,
      isFetchError: false,
      isInfo: false,
      splits: [],
      info: {}
    }
  },
  mounted () {
    this.fetchSplits()
  },
  methods: {
    fetchSplits () {
      this.isFetching = true
      this.isFetchError = false
      axios.get('/api/splits/fetch/').then((resp) => {
        let splits = []
        for (let s of resp.data) {
          let inc = 100 / s.contacts.length
          let prog = 0
          for (let c of s.contacts) {
            if (c.settled) {
              prog += inc
            }
          }
          splits.push({
            name: s.name,
            created_at: s.created_date,
            settled: s.settled,
            settlementProgress: prog,
            contacts: s.contacts,
            amount: s.amount
          })
        }
        this.splits = splits
      }).catch((_) => {
        this.isFetchError = true
      }).finally(() => {
        this.isFetching = false
      })
    },
    showInfo (split) {
      let settledContacts = []
      let pendingContacts = []
      for (let c of split.contacts) {
        if (c.settled) {
          settledContacts.push(c)
        } else {
          pendingContacts.push(c)
        }
      }

      this.info = {
        name: split.name,
        settled: split.settled,
        amount: split.amount,
        created_date: split.created_date,
        settled_contacts: settledContacts,
        pending_contacts: pendingContacts
      }
      this.isInfo = true
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
