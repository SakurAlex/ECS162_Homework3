import { vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/svelte'
import Comments from '../Comments.svelte'

const flat = [
  { _id:'a', content:'Root', parent:null },
  { _id:'b', content:'Child', parent:'a' }
]

describe('Comments.svelte', () => {
  it('nests replies correctly', () => {
    render(Comments, { props: { comments: flat, onSubmit: () => {} }})
    expect(screen.getByText('Root')).toBeInTheDocument()
    expect(screen.getByText('Child')).toBeInTheDocument()
    // Child should be rendered inside a nested <ul>
    const child = screen.getByText('Child')
    expect(child.closest('ul')).not.toBeNull()
  })

  it('emits event on reply submission', async () => {
    const mock = vi.fn()
    render(Comments, { props: { comments: [], onSubmit: mock } })

    await fireEvent.input(screen.getByRole('textbox'), { target: { value: 'hey' }})
    await fireEvent.click(screen.getByText('Submit'))

    expect(mock).toHaveBeenCalledWith({ content:'hey', parent:null })
  })
})
