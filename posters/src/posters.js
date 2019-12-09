import React, { useState, useEffect } from 'react';
import EventDropdown from './eventDropdown.js';
import TemplateDropdown from './templateDropdown.js';
import Poster from './poster.js';
const Posters = () => {
    const [regions, setRegions] = useState([])
    const [error, setError] = useState(null)
    const [loading, setLoading] = useState(false)

    const [posterRegion, setPosterRegion] = useState('');
    const [posterTemplate, setPosterTemplate] = useState("Blobs");
    const [posterFormat, setPosterFormat] = useState("svg");

    useEffect(() => {
        if (regions.length == 0) {
            fetch("https://clear.codeday.org/api/regions/")
                .then(res => res.json())
            .then(
                (result) => {
                    setLoading(true)
                    setRegions(result.filter(region => region.current_event != null))
                },
                (error) => {
                    setLoading(true)
                    setError(error)
                }
            )
        }
    })

    return(
        <>
            <h1>CodeDay Poster Generator</h1>
            <EventDropdown error={error} isLoading={loading} regions={regions} setRegion={setPosterRegion} />
            <Poster regions={regions} posterRegion={posterRegion} posterTemplate={posterTemplate} posterFormat={posterFormat}/>
        </>
    )
}
export default Posters