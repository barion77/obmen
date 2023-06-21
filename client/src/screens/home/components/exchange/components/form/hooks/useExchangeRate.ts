import { useEffect, useState } from "react"
import { serveUrl } from "../../../../../../../config"
import { useAppSelector } from "../../../../../../../store/hooks"

const config = {
    fromCurrenycRange: {
        from: 0.0013,
        to: 11
    },
    toCurrenycRange: {
        from: 0.0014,
        to: 15
    },
}

const getFixedAmount = (amount: number) => {
    if (amount.toFixed(7) === '0,0000000' || amount.toFixed(7) === '0.0000000') return '0'
    return amount.toFixed(7)
}

const useExchangeRate = () => {
    const {
        fromCurrency,
        toCurrency
    } = useAppSelector(state => state.exchange)

    const [fromCurrencyAmount, setFromCurrencyAmount] = useState('0.01')
    const [toCurrencyAmount, setToCurrencyAmount] = useState('')
    const [isChangeInput, setIsChangeInput] = useState(true)
    const [isChangeToCurrency, setIsChangeToCurrency] = useState(false)
    const [isChangeFromCurrency, setIsChangeFromCurrency] = useState(false)

    const getExchangeRate = async (toCurrencyAmount: string, fromCurrencyAmount: string, isChangeReceiveAmount: boolean) => {
        if (!isChangeInput || !toCurrency.shortName || !fromCurrency.shortName) return

        const isChange = isChangeReceiveAmount ? 'True' : 'false'
        const newForm = await fetch(`${serveUrl}/calculator/${fromCurrency.shortName}/${toCurrency.shortName}/${fromCurrencyAmount || '0.001'}/${toCurrencyAmount || '0.001'}/${isChange}`, {
            method: 'POST',
        }).then(res => res.json())

        if (isChangeReceiveAmount) {
            setFromCurrencyAmount(getFixedAmount(newForm.amount))
        } else {
            setToCurrencyAmount(getFixedAmount(newForm.amount))
        }
        setIsChangeInput(false)
    }

    useEffect(() => {
        getExchangeRate(toCurrencyAmount, fromCurrencyAmount, false)
    }, [fromCurrencyAmount, isChangeFromCurrency])

    useEffect(() => {
        getExchangeRate(toCurrencyAmount, fromCurrencyAmount, true)
    }, [toCurrencyAmount, isChangeToCurrency])

    useEffect(() => {
        setIsChangeInput(true)
        setIsChangeFromCurrency(prev => !prev)
    }, [fromCurrency])

    useEffect(() => {
        setIsChangeInput(true)
        setIsChangeToCurrency(prev => !prev)
    }, [toCurrency])

    const changeFromAmount = (amount: string) => {
        if (Number(amount) <= config.fromCurrenycRange.to && Number(amount) >= config.fromCurrenycRange.from) {
            setFromCurrencyAmount(amount)
        } else {
            setFromCurrencyAmount(`${config.fromCurrenycRange.from}`)
        }
    }

    const changeToAmount = (amount: string) => {
        if (Number(amount) <= config.toCurrenycRange.to && Number(amount) >= config.toCurrenycRange.from) {
            setFromCurrencyAmount(amount)
        } else {
            setFromCurrencyAmount(`${config.toCurrenycRange.from}`)
        }
    }

    return {
        exchangeRate: config,
        fromCurrencyAmount,
        toCurrencyAmount,
        setFromCurrencyAmount: changeFromAmount,
        setToCurrencyAmount: changeToAmount,
        setIsChangeInput
    }
}

export default useExchangeRate