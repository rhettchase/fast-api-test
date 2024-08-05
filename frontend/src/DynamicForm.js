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
    const questionId = parseInt(
      Object.keys(formData)[0].replace('question', '')
    ); // Extract integer ID
    const response = formData[`question${questionId}`]; // Access using template literal
    const payload = {
      question_id: questionId,
      response: response,
    };

    console.log('Submitting payload:', payload); // Log the payload for debugging
    dispatch(submitUserResponse(payload));
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

  return <Form schema={schema} onSubmit={handleSubmit} validator={validator} />;
}

export default DynamicForm;
