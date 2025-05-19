import { vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/svelte'
import Categories from '../Categories.svelte'

const cats = ['News','Opinion','Sports']

describe('Categories.svelte', () => {
  it('renders all categories and highlights selected', async () => {
    render(Categories, { props: { categories: cats, selected: 'News', onSelect: vi.fn() } })
    cats.forEach(c => expect(screen.getByText(c)).toBeInTheDocument())

    const sportBtn = screen.getByText('Sports')
    expect(sportBtn).not.toHaveClass('active')
    await fireEvent.click(sportBtn)
    expect(sportBtn).toHaveClass('active')
  })
})
