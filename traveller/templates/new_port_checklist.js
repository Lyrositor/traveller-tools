import {createApp} from 'https://unpkg.com/vue@3/dist/vue.esm-browser.prod.js'
import {dm, getHexInfo, selectText, TRADE_GOODS} from "./common.js";

const STARPORT_BROKER_DMS = {'A': 6, 'B': 4, 'C': 2, 'D': 0, 'E': 0, 'X': 0}

function getPurchaseDm(good, hexInfo) {
    const tradeInfo = TRADE_GOODS[good]
    return getTradeDm(tradeInfo.purchase_dms, good, hexInfo)
}

function getSaleDm(good, hexInfo) {
    const tradeInfo = TRADE_GOODS[good]
    let tradeDm = getTradeDm(tradeInfo.sale_dms, good, hexInfo)

    // Special case for goods which depend on the zone as well
    if (good === 22) {
        // Advanced Weapons
        if (hexInfo.zone === 'A') {
            tradeDm = Math.max(tradeDm, 2)
        } else if (hexInfo.zone === 'R') {
            tradeDm = Math.max(tradeDm, 4)
        }
    } else if (good === 62) {
        // Cybernetics, Illegal
        if (hexInfo.zone === 'A' || hexInfo.zone === 'R') {
            tradeDm = Math.max(tradeDm, 6)
        }
    } else if (good === 65) {
        // Weapons, Illegal
        if (hexInfo.zone === 'A') {
            tradeDm = Math.max(tradeDm, 8)
        } else if (hexInfo.zone === 'R') {
            tradeDm = Math.max(tradeDm, 10)
        }
    }

    return tradeDm
}

function getTradeDm(dms, good, hexInfo) {
    const applicableBonuses = []
    for (const [tradeCode, tradeDm] of Object.entries(dms)) {
        if (hexInfo.trade_codes.includes(tradeCode)) {
            applicableBonuses.push(tradeDm)
        }
    }
    if (applicableBonuses.length > 0) {
        return Math.max(...applicableBonuses)
    }
    return 0
}

function acquirePassengers(checkResult, steward, level, distance, additional, sourceHexInfo, destinationHexInfo) {
    const checkResultDm = dm(checkResult - 8)
    const stewardDm = dm(steward)

    let passengersDm = dm(0)
    if (level === 'High') {
        passengersDm = dm(-4)
    } else if (level === 'Low') {
        passengersDm = dm(1)
    }

    const sourcePopulationDm = dm(getPassengersWorldPopulationModifier(sourceHexInfo))
    const sourceStarportDm = dm(getPassengersWorldStarportModifier(sourceHexInfo))
    const sourceZoneDm = dm(getPassengersWorldZoneModifier(sourceHexInfo))
    const destPopulationDm = dm(getPassengersWorldPopulationModifier(destinationHexInfo))
    const destStarportDm = dm(getPassengersWorldStarportModifier(destinationHexInfo))
    const destZoneDm = dm(getPassengersWorldZoneModifier(destinationHexInfo))
    const distanceDm = dm(-distance)
    const additionalDm = dm(additional)

    return `!roll 2d6${checkResultDm}${stewardDm}${passengersDm}${sourcePopulationDm}${sourceStarportDm}${sourceZoneDm}${destPopulationDm}${destStarportDm}${destZoneDm}${distanceDm}${additionalDm}`
}

function getPassengersWorldPopulationModifier(hexInfo) {
    if (hexInfo.population <= 1) {
        return -4
    } else if (hexInfo.population >= 6 && hexInfo.population <= 7) {
        return 1
    } else if (hexInfo.population >= 8) {
        return 3
    } else {
        return 0
    }
}

function getPassengersWorldStarportModifier(hexInfo) {
    if (hexInfo.starport_quality === 'A') {
        return 2
    } else if (hexInfo.starport_quality === 'B') {
        return 1
    } else if (hexInfo.starport_quality === 'E') {
        return -1
    } else if (hexInfo.starport_quality === 'X') {
        return -3
    } else {
        return 0
    }
}

function getPassengersWorldZoneModifier(hexInfo) {
    if (hexInfo.zone === 'A') {
        return 1
    } else if (hexInfo.zone === 'R') {
        return -4
    } else {
        return 0
    }
}

function acquireFreight(checkResult, level, distance, additional, sourceHexInfo, destinationHexInfo) {
    return `!roll 2d6${getAcquireFreightModifiers(checkResult, level, distance, additional, sourceHexInfo, destinationHexInfo).map(modifier => dm(modifier)).join('')}`
}

function getAcquireFreightModifiers(checkResult, level, distance, additional, sourceHexInfo, destinationHexInfo) {
    let cargoModifier = 0
    if (level === 'Major') {
        cargoModifier = -4
    } else if (level === 'Incidental') {
        cargoModifier = 2
    }

    return [
        checkResult - 8,
        cargoModifier,
        getFreightWorldPopulationModifier(sourceHexInfo),
        getFreightWorldStarportModifier(sourceHexInfo),
        getFreightWorldTechModifier(sourceHexInfo),
        getFreightWorldZoneModifier(sourceHexInfo),
        getFreightWorldPopulationModifier(destinationHexInfo),
        getFreightWorldStarportModifier(destinationHexInfo),
        getFreightWorldTechModifier(destinationHexInfo),
        getFreightWorldZoneModifier(destinationHexInfo),
        -distance,
        additional,
    ]
}

function getFreightWorldPopulationModifier(hexInfo) {
    if (hexInfo.population <= 1) {
        return -4
    } else if (hexInfo.population >= 6 && hexInfo.population <= 7) {
        return 2
    } else if (hexInfo.population >= 8) {
        return 4
    } else {
        return 0
    }
}

function getFreightWorldStarportModifier(hexInfo) {
    if (hexInfo.starport_quality === 'A') {
        return 2
    } else if (hexInfo.starport_quality === 'B') {
        return 1
    } else if (hexInfo.starport_quality === 'E') {
        return -1
    } else if (hexInfo.starport_quality === 'X') {
        return -3
    } else {
        return 0
    }
}

function getFreightWorldTechModifier(hexInfo) {
    if (hexInfo.tech <= 6) {
        return -1
    } else if (hexInfo.tech >= 9) {
        return 2
    } else {
        return 0
    }
}

function getFreightWorldZoneModifier(hexInfo) {
    if (hexInfo.zone === 'A') {
        return -2
    } else if (hexInfo.zone === 'R') {
        return -6
    } else {
        return 0
    }
}

createApp({
    data() {
        return {
            tradeGoods: Object.values(TRADE_GOODS),
            newPort: {
                world: null,
                landing: {
                    characteristic: 0,
                    pilot: 0,
                    speed: false,
                    ship: 'streamlined',
                },
                sellGoods: {
                    broker: 0,
                    streetwise: 0,
                    admin: 0,
                    brokerCharacteristic: 0,
                    negotiationCharacteristic: 0,
                    previousAttempts: 0,
                    tradeGood: 11,
                    opposingBroker: 2,
                },
                buyGoods: {
                    broker: 0,
                    streetwise: 0,
                    admin: 0,
                    brokerCharacteristic: 0,
                    negotiationCharacteristic: 0,
                    previousAttempts: 0,
                    tradeGood: 11,
                    opposingBroker: 2,
                },
                acquirePassengers: {
                    destination: null,
                    checkResult: 0,
                    characteristic: 0,
                    skill: 0,
                    steward: 0,
                    distance: 0,
                    result: 0,
                    additional: 0,
                },
                acquireFreight: {
                    destination: null,
                    checkResult: 0,
                    characteristic: 0,
                    skill: 0,
                    distance: 0,
                    result: 0,
                    additional: 0
                },
                acquireMail: {
                    shipIsArmed: false,
                    highestNavalScoutRank: 0,
                    highestSoc: 0,
                }
            },
        }
    },
    computed: {
        newPortHexInfo() {
            return getHexInfo(this.newPort.world)
        },

        /* 1. Landing */
        newPortLandingRoll() {
            if (!this.newPortHexInfo) {
                return '(Choose world)'
            }

            let reason = 'Landing'

            const characteristicDm = dm(this.newPort.landing.characteristic)
            const pilotDm = dm(this.newPort.landing.pilot)
            let speedDm = dm(0)
            if (!this.newPort.landing.speed) {
                speedDm = dm(2)
                reason += ', careful'
            }
            let shipDm = dm(0)
            if (this.newPortHexInfo.atmosphere > 0) {
                if (this.newPort.landing.ship === 'partially-streamlined' && this.newPortHexInfo.atmosphere > 3) {
                    shipDm = dm(-2)
                    reason += ', partially streamlined'
                } else if (this.newPort.landing.ship === 'unstreamlined') {
                    shipDm = dm(-4)
                    reason += ', unstreamlined'
                }
            }

            return `!roll 2d6${characteristicDm}${pilotDm}${speedDm}${shipDm} !${reason}`
        },

        /* 3. Submit to Inspection */
        newPortInspectionRoll() {
            return `!roll 2d6 !Inspection`
        },

        /* 5. Sell Goods */
        starportBrokerDm() {
            return STARPORT_BROKER_DMS[this.newPortHexInfo?.starport_quality ?? 'X']
        },
        newPortSellGoodsFindBuyerInPersonRoll() {
            if (!this.newPortHexInfo) {
                return '(Choose world)'
            }
            const characteristicDm = dm(this.newPort.sellGoods.brokerCharacteristic)
            const brokerDm = dm(this.newPort.sellGoods.broker)
            const previousAttemptsDm = dm(-this.newPort.sellGoods.previousAttempts)
            const starportDm = dm(this.starportBrokerDm)
            return `!roll 2d6${characteristicDm}${brokerDm}${previousAttemptsDm}${starportDm} !Finding buyer/broker in person`
        },
        newPortSellGoodsFindBuyerOnlineRoll() {
            if (!this.newPortHexInfo) {
                return '(Choose world)'
            }
            const characteristicDm = dm(this.newPort.sellGoods.brokerCharacteristic)
            const adminDm = dm(this.newPort.sellGoods.admin)
            const previousAttemptsDm = dm(-this.newPort.sellGoods.previousAttempts)
            const starportDm = dm(this.starportBrokerDm)
            return `!roll 2d6${characteristicDm}${adminDm}${previousAttemptsDm}${starportDm} !Finding buyer/broker online`
        },
        newPortSellGoodsFindBuyerIllegalRoll() {
            if (!this.newPortHexInfo) {
                return '(Choose world)'
            }
            const characteristicDm = dm(this.newPort.sellGoods.brokerCharacteristic)
            const streetwiseDm = dm(this.newPort.sellGoods.streetwise)
            const previousAttemptsDm = dm(-this.newPort.sellGoods.previousAttempts)
            const starportDm = dm(this.starportBrokerDm)
            return `!roll 2d6${characteristicDm}${streetwiseDm}${previousAttemptsDm}${starportDm} !Finding black market buyer/broker`
        },
        newPortSellGoodsNegotiationRoll() {
            if (!this.newPortHexInfo || !this.newPort.sellGoods.tradeGood) {
                return '(Choose world)'
            }
            const characteristicDm = dm(this.newPort.sellGoods.negotiationCharacteristic)
            const brokerDm = dm(this.newPort.sellGoods.broker)
            const tradeGoodInfo = TRADE_GOODS[this.newPort.sellGoods.tradeGood]
            const saleDm = dm(getSaleDm(this.newPort.sellGoods.tradeGood, this.newPortHexInfo))
            const purchaseDm = dm(-getPurchaseDm(this.newPort.sellGoods.tradeGood, this.newPortHexInfo))
            const opposingBrokerDm = dm(-this.newPort.sellGoods.opposingBroker)
            return `!roll 3d6${characteristicDm}${brokerDm}${saleDm}${purchaseDm}${opposingBrokerDm} !Negotiating sale price for ${tradeGoodInfo.name} on ${this.newPortHexInfo.name}`
        },

        /* 6. Acquire Passengers */
        newPortAcquirePassengersDestinationHexInfo() {
            return getHexInfo(this.newPort.acquirePassengers.destination)
        },
        newPortAcquirePassengersCheckRoll() {
            return `!roll 2d6${dm(this.newPort.acquirePassengers.characteristic)}${dm(this.newPort.acquirePassengers.skill)} !Determining passengers check DM`
        },
        newPortAcquirePassengersHighRoll() {
            return this.newPortAcquirePassengersRoll('High')
        },
        newPortAcquirePassengersMiddleRoll() {
            return this.newPortAcquirePassengersRoll('Middle')
        },
        newPortAcquirePassengersBasicRoll() {
            return this.newPortAcquirePassengersRoll('Basic')
        },
        newPortAcquirePassengersLowRoll() {
            return this.newPortAcquirePassengersRoll('Low')
        },
        newPortAcquirePassengersNumRoll() {
            let result
            if (this.newPort.acquirePassengers.result <= 1) {
                result = 0
            } else if (this.newPort.acquirePassengers.result <= 3) {
                result = 1
            } else if (this.newPort.acquirePassengers.result <= 6) {
                result = 2
            } else if (this.newPort.acquirePassengers.result <= 10) {
                result = 3
            } else if (this.newPort.acquirePassengers.result <= 13) {
                result = 4
            } else if (this.newPort.acquirePassengers.result <= 15) {
                result = 5
            } else if (this.newPort.acquirePassengers.result <= 16) {
                result = 6
            } else if (this.newPort.acquirePassengers.result <= 17) {
                result = 7
            } else if (this.newPort.acquirePassengers.result <= 18) {
                result = 8
            } else if (this.newPort.acquirePassengers.result <= 19) {
                result = 9
            } else {
                result = 10
            }
            return `!roll ${result}d6 !Number of passengers`
        },

        /* 7. Acquire Freight */
        newPortAcquireFreightDestinationHexInfo() {
            return getHexInfo(this.newPort.acquireFreight.destination)
        },
        newPortAcquireFreightCheckRoll() {
            return `!roll 2d6${dm(this.newPort.acquireFreight.characteristic)}${dm(this.newPort.acquireFreight.skill)} !Determining freight check DM`
        },
        newPortAcquireFreightMajorRoll() {
            return this.newPortAcquireFreightRoll('Major')
        },
        newPortAcquireFreightMinorRoll() {
            return this.newPortAcquireFreightRoll('Minor')
        },
        newPortAcquireFreightIncidentalRoll() {
            return this.newPortAcquireFreightRoll('Incidental')
        },
        newPortAcquireFreightNumRoll() {
            let result
            if (this.newPort.acquireFreight.result <= 1) {
                result = 0
            } else if (this.newPort.acquireFreight.result <= 3) {
                result = 1
            } else if (this.newPort.acquireFreight.result <= 5) {
                result = 2
            } else if (this.newPort.acquireFreight.result <= 8) {
                result = 3
            } else if (this.newPort.acquireFreight.result <= 11) {
                result = 4
            } else if (this.newPort.acquireFreight.result <= 14) {
                result = 5
            } else if (this.newPort.acquireFreight.result <= 16) {
                result = 6
            } else if (this.newPort.acquireFreight.result <= 17) {
                result = 7
            } else if (this.newPort.acquireFreight.result <= 18) {
                result = 8
            } else if (this.newPort.acquireFreight.result <= 19) {
                result = 9
            } else {
                result = 10
            }
            return `!roll ${result}d6 !Number of freight lots`
        },

        /* 8. Acquire Mail */
        newPortAcquireMailRoll() {
            if (!this.newPortHexInfo || !this.newPortAcquireFreightDestinationHexInfo) {
                return '(Choose origin and destination worlds)'
            }

            const freightTrafficModifier = getAcquireFreightModifiers(
                this.newPort.acquireFreight.checkResult,
                'minor',
                this.newPort.acquireFreight.distance,
                this.newPort.acquireFreight.additional,
                this.newPortHexInfo,
                this.newPortAcquireFreightDestinationHexInfo,
            ).reduce((partialSum, a) => partialSum + a, 0)
            let freightTrafficDm
            if (freightTrafficModifier <= -10) {
                freightTrafficDm = dm(-2)
            } else if (freightTrafficModifier <= -5) {
                freightTrafficDm = dm(-1)
            } else if (freightTrafficModifier <= 4) {
                freightTrafficDm = dm(0)
            } else if (freightTrafficModifier <= 9) {
                freightTrafficDm = dm(1)
            } else {
                freightTrafficDm = dm(2)
            }

            let shipIsArmedDm = dm(0)
            if (this.newPort.acquireMail.shipIsArmed) {
                shipIsArmedDm = dm(2)
            }

            let techDm = dm(0)
            if (this.newPortAcquireFreightDestinationHexInfo.tech <= 5) {
                techDm = dm(-4)
            }

            let highestNavalOrScoutRankDm = dm(this.newPort.acquireMail.highestNavalScoutRank)
            let highestSocDm = dm(this.newPort.acquireMail.highestSoc)
            return `!roll 2d6${freightTrafficDm}${shipIsArmedDm}${techDm}${highestNavalOrScoutRankDm}${highestSocDm}`
        },

        /* 9. Buy Goods */
        newPortBuyGoodsFindBuyerInPersonRoll() {
            if (!this.newPortHexInfo) {
                return '(Choose world)'
            }
            const characteristicDm = dm(this.newPort.buyGoods.brokerCharacteristic)
            const brokerDm = dm(this.newPort.buyGoods.broker)
            const previousAttemptsDm = dm(-this.newPort.buyGoods.previousAttempts)
            const starportDm = dm(this.starportBrokerDm)
            return `!roll 2d6${characteristicDm}${brokerDm}${previousAttemptsDm}${starportDm} !Finding supplier/broker in person`
        },
        newPortBuyGoodsFindBuyerOnlineRoll() {
            if (!this.newPortHexInfo) {
                return '(Choose world)'
            }
            const characteristicDm = dm(this.newPort.buyGoods.brokerCharacteristic)
            const adminDm = dm(this.newPort.buyGoods.admin)
            const previousAttemptsDm = dm(-this.newPort.buyGoods.previousAttempts)
            const starportDm = dm(this.starportBrokerDm)
            return `!roll 2d6${characteristicDm}${adminDm}${previousAttemptsDm}${starportDm} !Finding supplier/broker online`
        },
        newPortBuyGoodsFindBuyerIllegalRoll() {
            if (!this.newPortHexInfo) {
                return '(Choose world)'
            }
            const characteristicDm = dm(this.newPort.buyGoods.brokerCharacteristic)
            const streetwiseDm = dm(this.newPort.buyGoods.streetwise)
            const previousAttemptsDm = dm(-this.newPort.buyGoods.previousAttempts)
            const starportDm = dm(this.starportBrokerDm)
            return `!roll 2d6${characteristicDm}${streetwiseDm}${previousAttemptsDm}${starportDm} !Finding black market supplier/broker`
        },
        newPortBuyGoodsNegotiationRoll() {
            if (!this.newPortHexInfo || !this.newPort.buyGoods.tradeGood) {
                return '(Choose world)'
            }
            const characteristicDm = dm(this.newPort.buyGoods.negotiationCharacteristic)
            const brokerDm = dm(this.newPort.buyGoods.broker)
            const tradeGoodInfo = TRADE_GOODS[this.newPort.buyGoods.tradeGood]
            const purchaseDm = dm(getPurchaseDm(this.newPort.buyGoods.tradeGood, this.newPortHexInfo))
            const saleDm = dm(-getSaleDm(this.newPort.buyGoods.tradeGood, this.newPortHexInfo))
            const opposingBrokerDm = dm(-this.newPort.buyGoods.opposingBroker)
            return `!roll 3d6${characteristicDm}${brokerDm}${purchaseDm}${saleDm}${opposingBrokerDm} !Negotiating purchase price for ${tradeGoodInfo.name} on ${this.newPortHexInfo.name}`
        },
    },
    methods: {
        newPortAcquirePassengersRoll(level) {
            if (!this.newPortHexInfo || !this.newPortAcquirePassengersDestinationHexInfo) {
                return '(Choose origin and destination worlds)'
            }
            return acquirePassengers(
                this.newPort.acquirePassengers.checkResult,
                this.newPort.acquirePassengers.steward,
                level,
                this.newPort.acquirePassengers.distance,
                this.newPort.acquirePassengers.additional,
                this.newPortHexInfo,
                this.newPortAcquirePassengersDestinationHexInfo
            ) + ` !Acquiring ${level} passengers from ${this.newPortHexInfo.name} to ${this.newPortAcquirePassengersDestinationHexInfo.name}`
        },

        newPortAcquireFreightRoll(level) {
            if (!this.newPortHexInfo || !this.newPortAcquireFreightDestinationHexInfo) {
                return '(Choose origin and destination worlds)'
            }
            return acquireFreight(
                this.newPort.acquireFreight.checkResult,
                level,
                this.newPort.acquireFreight.distance,
                this.newPort.acquireFreight.additional,
                this.newPortHexInfo,
                this.newPortAcquireFreightDestinationHexInfo
            ) + ` !Acquiring ${level} freight from ${this.newPortHexInfo.name} to ${this.newPortAcquireFreightDestinationHexInfo.name}`
        },
    },
    mounted() {
        $('code').on("click", function () {
            selectText(this)
        })
    },
}).mount('#app')
