import React, { useState } from "react";

export default props => {
  return (
    <div class="promoInfo">
      Use promo code
      <input
        type="text"
        value={props.promo}
        placeholder="YOURCODE"
        onChange={e => props.setPromo(e.target.value)}
        />
      for
      <input
        type="text"
        value={props.promoFor}
        placeholder="20% off"
        onChange={e => props.setPromoFor(e.target.value)}
        />
    </div>
  )
};
