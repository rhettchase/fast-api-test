import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Form from '@rjsf/core';
import {
  fetchFormConfig,
  submitUserResponse,
  setUserResponse,
} from './formSlice';
import validator from '@rjsf/validator-ajv8';

function DynamicForm() {
  const dispatch = useDispatch();
  const { currentFormId, formConfig, message } = useSelector(
    (state) => state.form
  );

  useEffect(() => {
    dispatch(fetchFormConfig(currentFormId));
  }, [currentFormId, dispatch]);

  const handleSubmit = ({ formData }) => {
    const questionId = Object.keys(formData)[0];
    dispatch(setUserResponse({ questionId, response: formData[questionId] }));
    dispatch(
      submitUserResponse({ questionId, response: formData[questionId] })
    );
  };

  if (message) {
    return <div>{message}</div>;
  }

  if (!formConfig) {
    return <div>Loading...</div>;
  }

  const schema = {
    title: formConfig.title,
    type: 'object',
    properties: formConfig.fields.reduce((acc, field) => {
      acc[field.name] = {
        type: field.type,
        title: field.label,
        enum: field.options,
      };
      return acc;
    }, {}),
  };

  return <Form schema={schema} onSubmit={handleSubmit} validator={validator} />; // Pass the validator prop
}

export default DynamicForm;
