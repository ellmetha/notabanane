/* eslint jsx-a11y/label-has-for: 0 */
/* eslint react/prop-types: 0 */

import React from 'react';


const Label = ({ error, children, ...props }) => (
  <label {...props}>{children}</label>
);

const CheckBox = ({
  field: { name, ...field },
  form: { errors },
  className,
  id,
  label,
  helpText,
  ...props
}) => {
  const error = errors[name];
  return (
    <Label htmlFor={id || name} error={error} className="checkbox">
      <input
        key={`key-${id || name}`}
        id={id || name}
        name={name}
        type="checkbox"
        checked={field.value}
        {...field}
        {...props}
      />
      <span className="label" />
      <span className="label-text">{label}</span>
    </Label>
  );
};

export default CheckBox;
