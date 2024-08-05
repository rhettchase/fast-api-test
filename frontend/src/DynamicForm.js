import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Form from '@rjsf/core';
import {
  fetchFormConfig,
  submitUserResponse,
  setUserResponse,
  fetchNextQuestion,
  setMessage,
  clearFormConfig,
} from './formSlice';
import validator from '@rjsf/validator-ajv8';

function DynamicForm() {
  const dispatch = useDispatch();
  const { currentFormId, formConfig, message, userResponse } = useSelector(
    (state) => state.form
  );

  useEffect(() => {
    if (currentFormId !== null) {
      dispatch(fetchFormConfig(currentFormId));
    }
  }, [currentFormId, dispatch]);

  useEffect(() => {
    if (userResponse) {
      console.log('User response:', userResponse); // Log whenever userResponse changes
    }
  }, [userResponse]);

  const handleSubmit = async ({ formData }) => {
    const questionId = parseInt(
      Object.keys(formData)[0].replace('question', '')
    ); // Extract integer ID
    const response = formData[`question${questionId}`]; // Access using template literal
    const payload = {
      question_id: questionId,
      response: response,
    };

    console.log('Submitting payload:', payload);
    
    // Await dispatch actions to ensure state updates before logging
    await dispatch(setUserResponse(payload)); // Set user response

    // Highlight: Awaiting dispatch actions for sequential updates
    await dispatch(submitUserResponse(payload));
    const result = await dispatch(fetchNextQuestion(payload));

    // Handle the result of fetching the next question
    if (
      result.payload &&
      typeof result.payload === 'object' &&
      result.payload.message
    ) {
      dispatch(setMessage(result.payload.message));
      dispatch(clearFormConfig()); // Clear form config if no more questions
    }
  };

  if (message) {
    return <div>{message}</div>;
  }

  if (!formConfig || !formConfig.fields) {
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
