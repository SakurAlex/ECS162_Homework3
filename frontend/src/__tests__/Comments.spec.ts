import { test, expect } from 'vitest'
import { render, screen } from '@testing-library/svelte'
import Comments from '../Comments.svelte'

test('Comments shows user and content', () => {
  const comment = { 
    id: '1', 
    user: 'Alice', 
    content: 'Hi', 
    removed: false 
}
  render(Comments, { props: { comment } })
  expect(screen.getByText('Alice')).toBeInTheDocument()
  expect(screen.getByText('Hi')).toBeInTheDocument()
})
