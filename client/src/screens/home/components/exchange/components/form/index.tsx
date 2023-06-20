import { useEffect, useRef, useState } from "react"
import { useAppSelector } from "../../../../../../store/hooks"
import useExchangeRate from "./hooks/useExchangeRate"
import Captcha from "./components/captcha"
import Email from "./components/email"
import Receiver from "./components/receiver"
import ReferalCode from "./components/referalCode"
import useForm from "./hooks/useForm"

const Form = () => {
    const {
        fromCurrency,
        toCurrency,
    } = useAppSelector(state => state.exchange)

    const {
        exchangeRate,
        toCurrencyAmount,
        fromCurrencyAmount,
        setFromCurrencyAmount,
        setToCurrencyAmount,
        setIsChangeInput
    } = useExchangeRate()

    const {
        sendForm,
    } = useForm()

    return (
        <form onSubmit={async (e) => await sendForm(e, fromCurrencyAmount, toCurrencyAmount)} className="exchange__block-form">
            <div className="exchange__block-wrapper">
                <div className="exchange__block-text exchange__block-text-send">
                    You send <span>({exchangeRate.fromCurrenycRange.from} — {exchangeRate.fromCurrenycRange.to})</span>
                </div>
                <div className="exchange__block-header exchange__block-header-send">
                    {fromCurrency.fullName}
                </div>
                <input
                    className="exchange__block-input exchange__block-input-val exchange__block-input-send"
                    type="number"
                    step="any"
                    value={fromCurrencyAmount}
                    onChange={e => {
                        setIsChangeInput(true)
                        setFromCurrencyAmount(e.target.value)
                    }}
                />
            </div>
            <div className="exchange__block-wrapper">
                <div className="exchange__block-text exchange__block-text-receive">
                    You receive <span>({exchangeRate.toCurrenycRange.from} — {exchangeRate.toCurrenycRange.to})</span>
                </div>
                <div className="exchange__block-header exchange__block-header-receive">
                    {toCurrency.fullName}
                </div>
                <input
                    className="exchange__block-input exchange__block-input-val exchange__block-input-receive"
                    type="number"
                    step="any"
                    value={toCurrencyAmount}
                    onChange={e => {
                        setIsChangeInput(true)
                        setToCurrencyAmount(e.target.value)
                    }}
                />
            </div>
            <Receiver />
            <Email />
            <ReferalCode />
            <Captcha />
            <button className="exchange__block-btn">Continue</button>
        </form>
    )
}

export default Form