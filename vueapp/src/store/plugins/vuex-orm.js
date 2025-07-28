import VuexORM from '@vuex-orm/core'
import Comp from '../../models/Comp'

// Create a new instance of Database
const database = new VuexORM.Database()

// Register Models to Database
database.register(Comp)

export default VuexORM.install(database)